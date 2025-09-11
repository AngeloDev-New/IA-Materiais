from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
import face_recognition
import json
import base64
import io
from PIL import Image
import numpy as np
from datetime import datetime
import hashlib
from .models import Foto

# Cache de faces conhecidas carregadas do banco
known_faces_cache = {}

def load_known_faces():
    """Carrega faces conhecidas do banco de dados para o cache"""
    global known_faces_cache
    
    # Se o cache já está carregado, não recarrega
    if known_faces_cache:
        return
    
    fotos = Foto.objects.all()
    for foto in fotos:
        try:
            # Carregar a imagem e gerar o encoding
            image = Image.open(foto.imagem.path)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            image_array = np.array(image)
            face_encodings = face_recognition.face_encodings(image_array)
            
            if face_encodings:  # Se encontrou pelo menos uma face
                known_faces_cache[str(foto.ide)] = {
                    'encoding': face_encodings[0],  # Pega a primeira face encontrada
                    'foto_id': foto.id,
                    'created_at': foto.criado_em.isoformat()
                }
        except Exception as e:
            print(f"Erro ao carregar foto {foto.id}: {e}")

def index(request):
    return render(request, 'api/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request):
    # Carrega faces conhecidas do banco se necessário
    load_known_faces()
    
    try:
        # Decodificar JSON do body
        data = json.loads(request.body)
        frame_data = data.get('frame')
        
        if not frame_data:
            return JsonResponse({'error': 'Frame não encontrado'}, status=400)
        
        # Decodificar base64 para imagem
        image = decode_base64_image(frame_data)
        if image is None:
            return JsonResponse({'error': 'Erro ao decodificar imagem'}, status=400)
        
        # Converter PIL para numpy array (RGB)
        image_array = np.array(image)
        
        # Detectar faces na imagem
        face_locations = face_recognition.face_locations(image_array)
        face_encodings = face_recognition.face_encodings(image_array, face_locations)
        
        detected_faces = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Extrair a face da imagem
            top, right, bottom, left = face_location
            face_image = image.crop((left, top, right, bottom))
            
            # Verificar se é uma face conhecida
            matched_person_id, confidence = find_matching_person(face_encoding)
            
            if matched_person_id is None:
                # É uma pessoa nova - salvar no banco
                person_id = save_new_person(face_image, face_encoding)
                confidence = 0.85  # Confiança inicial para pessoa nova
            else:
                person_id = matched_person_id
            
            # Converter face para base64 para retorno
            face_base64 = pil_to_base64(face_image)
            
            face_data = {
                'id': person_id,
                'profile_image': face_base64,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'bbox': {
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top
                },
                'is_new': matched_person_id is None
            }
            
            detected_faces.append(face_data)
        
        return JsonResponse({
            'faces': detected_faces,
            'total_detected': len(detected_faces)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

def find_matching_person(face_encoding):
    """
    Procura por uma pessoa conhecida comparando encodings
    Retorna (person_id, confidence) ou (None, None) se não encontrar
    """
    best_match_id = None
    best_confidence = 0
    tolerance = 0.6  # Tolerância para considerar como mesma pessoa
    
    for person_id, data in known_faces_cache.items():
        known_encoding = data['encoding']
        
        # Calcular distância entre encodings
        distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
        
        # Se distância é pequena o suficiente, é provavelmente a mesma pessoa
        if distance < tolerance:
            confidence = 1.0 - distance  # Converter distância em confiança
            
            # Manter o melhor match (menor distância = maior confiança)
            if confidence > best_confidence:
                best_confidence = confidence
                best_match_id = person_id
    
    if best_match_id is not None:
        return best_match_id, min(best_confidence, 0.99)
    
    return None, None

def save_new_person(face_image, face_encoding):
    """
    Salva uma nova pessoa no banco de dados
    Retorna o ID da pessoa criada
    """
    try:
        # Gerar um novo ID único
        new_id = generate_unique_person_id()
        
        # Converter imagem PIL para arquivo que pode ser salvo no Django
        buffer = io.BytesIO()
        face_image.save(buffer, format='JPEG', quality=95)
        buffer.seek(0)
        
        # Criar nome do arquivo
        filename = f"person_{new_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        # Criar objeto Foto e salvar
        foto = Foto()
        foto.ide = new_id
        foto.imagem.save(filename, ContentFile(buffer.getvalue()), save=True)
        
        # Adicionar ao cache
        known_faces_cache[str(new_id)] = {
            'encoding': face_encoding,
            'foto_id': foto.id,
            'created_at': foto.criado_em.isoformat()
        }
        
        print(f"Nova pessoa salva: ID {new_id}")
        return str(new_id)
        
    except Exception as e:
        print(f"Erro ao salvar nova pessoa: {e}")
        return str(generate_unique_person_id())  # Retorna ID mesmo se falhar o salvamento

def generate_unique_person_id():
    """Gera um ID único para uma nova pessoa"""
    # Pega o maior ID existente e adiciona 1
    existing_ids = []
    
    # Verificar IDs no cache
    for person_id in known_faces_cache.keys():
        try:
            existing_ids.append(int(person_id))
        except ValueError:
            pass
    
    # Verificar IDs no banco (caso o cache não esteja completo)
    try:
        max_id_from_db = Foto.objects.all().aggregate(
            max_id=models.Max('ide')
        )['max_id']
        if max_id_from_db:
            existing_ids.append(max_id_from_db)
    except:
        pass
    
    if existing_ids:
        return max(existing_ids) + 1
    else:
        return 1  # Primeira pessoa

def decode_base64_image(base64_string):
    """Decodifica string base64 para imagem PIL"""
    try:
        # Remove o prefixo data:image/...;base64, se existir
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decodifica base64
        image_data = base64.b64decode(base64_string)
        
        # Converte para PIL Image
        image = Image.open(io.BytesIO(image_data))
        
        # Converte para RGB se necessário
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        return image
    except Exception as e:
        print(f"Erro ao decodificar imagem: {e}")
        return None

def pil_to_base64(pil_image):
    """Converte imagem PIL para base64"""
    try:
        buffer = io.BytesIO()
        pil_image.save(buffer, format='JPEG', quality=85)
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/jpeg;base64,{img_str}"
    except Exception as e:
        print(f"Erro ao converter para base64: {e}")
        return ""

@require_http_methods(["GET"])
def get_profiles(request):
    """Endpoint para listar todas as faces conhecidas"""
    load_known_faces()  # Garantir que o cache está carregado
    
    profiles = []
    
    # Buscar dados do banco para ter informações completas
    fotos = Foto.objects.all().order_by('-criado_em')
    
    for foto in fotos:
        try:
            # Gerar base64 da imagem
            with foto.imagem.open() as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode()
                profile_image = f"data:image/jpeg;base64,{img_base64}"
            
            profiles.append({
                'id': str(foto.ide),
                'profile_image': profile_image,
                'first_seen': foto.criado_em.isoformat(),
                'last_seen': foto.criado_em.isoformat()  # Por enquanto, mesmo valor
            })
        except Exception as e:
            print(f"Erro ao carregar perfil {foto.id}: {e}")
    
    return JsonResponse({'profiles': profiles})

@csrf_exempt
@require_http_methods(["POST"])
def reset_faces(request):
    """Endpoint para limpar todas as faces conhecidas (útil para testes)"""
    global known_faces_cache
    
    try:
        # Limpar cache
        known_faces_cache.clear()
        
        # Opcional: deletar do banco também
        # Foto.objects.all().delete()
        
        return JsonResponse({'message': 'Cache limpo com sucesso'})
    except Exception as e:
        return JsonResponse({'error': f'Erro ao limpar cache: {str(e)}'}, status=500)