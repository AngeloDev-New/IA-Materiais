from django.db import models

# Create your models here.
class  Cameras(models.Model):
    # campos = ['nome', 'url_stream', 'latitude', 'longitude', 'direction', 'alcance']
    nome = models.CharField(max_length=45)
    url_stream = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    direction = models.IntegerField()
    alcance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    