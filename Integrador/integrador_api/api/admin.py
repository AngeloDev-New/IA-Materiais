from django.contrib import admin
from .models import Cameras
# Register your models here.
class CameraAdmin(admin.ModelAdmin):
    ...
admin.site.register(Cameras,CameraAdmin)