from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-frame', views.process_frame, name='process_frame'),
    path('api/profiles', views.get_profiles, name='get_profiles'), 
]
