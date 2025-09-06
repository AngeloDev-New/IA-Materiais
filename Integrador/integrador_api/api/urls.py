from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.map_view),
    path('map/',views.map_view),
    path('points/',views.points_view),
    path('enginepng/',views.image_route('assets/conf.png')),
    path('cameras/',views.camera_view),
    path('camera/<int:camera_id>/',views.camera, name='camera')

]
