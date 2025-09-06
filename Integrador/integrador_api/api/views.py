from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
import cv2
# from .CameraClass  import Camera
from .models import Cameras
from PIL import Image
import io
import os
import json
def getFrameFromLink(link,recise = None):
    ret, frame = cv2.VideoCapture(link)
    if recise:
            frame = cv2.resize(frame, recise)
    if not ret:
        raise Exception("Não consegui capturar frame")
    return frame
# Rota que retorna os pontos em JSON
def getCarsInCameraFromId(id):
    # Exemplo de retorno de carros
    # [
    #     {"lat": -25.509495, "lng": -54.599215}, 
    #     {"lat": -25.509497, "lng": -54.600273}, 
    #     {"lat": -25.509499, "lng": -54.601331}, 
    #     {"lat": -25.509501, "lng": -54.602389}  
    # ]

    return []

def camera(request,camera_id):
    try:
        camera_requisitada = Cameras.objects.get(id=camera_id)
    except:
        return HttpResponse(status = 405)
    
    contexto = {
        'm3u8':camera_requisitada.url_stream
    }
    return render(request, "api/camera.html", contexto)
def points_view(request):
    cameras = Cameras.objects.all()
    pontos = [{
        'lat': camera.latitude,
        'lng': camera.longitude,
        'nome': camera.nome,
        'cars':getCarsInCameraFromId(camera.id)
    }
              for camera in cameras]
    return JsonResponse(pontos, safe=False)

def image_route(path_img):
    path_img = os.path.join(settings.BASE_DIR, path_img)
    def view(request):
        img = Image.open(path_img)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return HttpResponse(buffer, content_type="image/png")
    return view
def map_view(request):
    return render(request, 'api/map.html')
@csrf_exempt
def camera_view(request):
    if (request.method == 'POST'):
        try:
            dados = json.loads(request.body)
            camera = Cameras.objects.create(
                nome=dados.get("nome"),
                url_stream=dados.get("url_stream"),
                latitude=dados.get("latitude"),
                longitude=dados.get("longitude"),
                direction=dados.get("direction"),
                alcance=dados.get("alcance")
            )

            return JsonResponse({
                "message": "Câmera adicionada com sucesso!",
                "camera_id": camera.id
            })
            return JsonResponse({"message": "Câmera adicionada com sucesso!"})
        except:
            return HttpResponse(status = 400)
    return HttpResponse(status = 405)