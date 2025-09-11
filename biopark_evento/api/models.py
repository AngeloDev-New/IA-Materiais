from django.db import models

class Foto(models.Model):
    # Um campo para salvar a imagem
    imagem = models.ImageField(upload_to='imagens/')  # vai salvar em MEDIA_ROOT/imagens/
    
    # Um campo para guardar um ID (pode ser relacionado a outro model ou apenas um inteiro)
    ide = models.IntegerField()  # ou models.CharField(max_length=100) se for string
    
    # Opcional: quando foi criado
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Foto {self.id} - IDE {self.ide}"
