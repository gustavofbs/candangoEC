from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.sessions.models import Session

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = CloudinaryField('imagem', blank=True, null=True)

    def __str__(self):
        return self.nome

class ItemCarrinho(models.Model):
    session_key = models.CharField(max_length=40)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session_key', 'produto')
        ordering = ['-data_adicionado']
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
    def subtotal(self):
        return self.quantidade * self.produto.preco
