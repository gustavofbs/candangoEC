from django.db import models
from cloudinary.models import CloudinaryField

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = CloudinaryField('imagem', blank=True, null=True)

    def __str__(self):
        return self.nome
