from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import face_recognition
import json
import base64
import io
from PIL import Image
import numpy as np
from datetime import datetime
import hashlib

known_faces = {}

def index(request):
    return render(request, 'api/index.html')

@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request):
    # print (known_faces)
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
            
            # Gerar ID único para a face baseado no encoding
            face_id = generate_face_id(face_encoding)
        
            # Verificar se é uma face conhecida
            is_known_face, confidence = match_known_face(face_encoding, face_id)
            
            # Converter face para base64
            face_base64 = pil_to_base64(face_image)
            
            face_data = {
                'id': face_id,
                'profile_image': face_base64,
                'confidence': confidence,
                'timestamp': datetime.now().isoformat(),
                'bbox': {
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top
                }
            }
            
            detected_faces.append(face_data)
            
            # Armazenar face se for nova ou atualizar confiança
            if not is_known_face or confidence > known_faces.get(face_id, {}).get('confidence', 0):
                known_faces[face_id] = {
                    'encoding': face_encoding,
                    'profile_image': face_base64,
                    'confidence': confidence,
                    'first_seen': known_faces.get(face_id, {}).get('first_seen', datetime.now().isoformat()),
                    'last_seen': datetime.now().isoformat()
                }
        
        return JsonResponse({
            'faces': detected_faces,
            'total_detected': len(detected_faces)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Erro interno: {str(e)}'}, status=500)

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

def generate_face_id(face_encoding):
    """Gera ID único para uma face baseado no encoding"""
    # Converte encoding para string e gera hash
    encoding_str = ','.join(map(str, face_encoding.round(6)))
    return hashlib.md5(encoding_str.encode()).hexdigest()[:12]

def match_known_face(face_encoding, face_id):
    """Verifica se a face já é conhecida e retorna confiança"""
    if face_id in known_faces:
        return True, 0.95  # Face conhecida, alta confiança
    
    # Comparar com faces conhecidas usando tolerância
    for known_id, known_data in known_faces.items():
        known_encoding = known_data['encoding']
        
        # Calcular distância entre encodings
        distance = face_recognition.face_distance([known_encoding], face_encoding)[0]
        
        # Se distância é pequena, é provavelmente a mesma pessoa
        if distance < 0.6:  # Tolerância padrão
            confidence = 1.0 - distance  # Converter distância em confiança
            return True, min(confidence, 0.99)
    
    # Face nova
    return False, 0.85

@require_http_methods(["GET"])
def get_profiles(request):
    """Endpoint opcional para listar todas as faces conhecidas"""
    profiles = []
    
    for face_id, data in known_faces.items():
        profiles.append({
            'id': face_id,
            'profile_image': data['profile_image'],
            'confidence': data['confidence'],
            'first_seen': data['first_seen'],
            'last_seen': data['last_seen']
        })
    
    # Ordenar por última detecção
    profiles.sort(key=lambda x: x['last_seen'], reverse=True)
    
    return JsonResponse({'profiles': profiles})