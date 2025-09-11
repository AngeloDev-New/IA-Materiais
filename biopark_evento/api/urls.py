from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-frame', views.process_frame, name='process_frame'),
    path('api/get-profiles', views.get_profiles, name='get_profiles'),
    path('api/reset-faces', views.reset_faces, name='reset_faces'),
    path('api/clear-all-faces', views.clear_all_faces, name='clear_all_faces'),  # Nova
    path('galeria/', views.galeria, name='galeria'),  # Renomeada
    path('delete/<int:foto_id>/', views.delete_photo, name='delete_photo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

