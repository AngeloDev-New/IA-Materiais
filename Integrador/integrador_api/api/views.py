from django.shortcuts import render
from django.http import JsonResponse
# utils.py
from django.http import HttpResponse
from PIL import Image
import io
import os
from django.conf import settings
from . import CameraClass as c
import json
# Página do mapa

# linkStream = 'https://video04.logicahost.com.br/portovelhomamore/fozpontedaamizadesentidoparaguai.stream/playlist.m3u8'
# camera = c.Camera(linkStream)
def map_view(request):
    return render(request, 'api/map.html')
# @csrf_exempt
def camera_view(request):
    if (request.method == 'POST'):
        try:
            data = json.loads(request.body)
            ...
            return HttpResponse(status = 201)
        except:
            return HttpResponse(status = 400)
    return HttpResponse(status = 405)
# Rota que retorna os pontos em JSON
def points_view(request):

    pontos = [

        # biopark
        # {'lat': -24.6176737, 'lng': -53.710399, 'nome': 'Biopark Toledo'},
        {
            'lat': -25.50949500,
            'lng': -54.599215,
            'nome': 'ponte_aduana',
               'cars': [
    {"lat": -25.509495, "lng": -54.599215}, 
    {"lat": -25.509497, "lng": -54.600273}, 
    {"lat": -25.509499, "lng": -54.601331}, 
    {"lat": -25.509501, "lng": -54.602389}  
                ]
        },
     

    ]
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