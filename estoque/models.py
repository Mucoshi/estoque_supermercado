from django.db import models

CATEGORIAS = [
    ('alimentos', 'Alimentos'),
    ('limpeza', 'Produtos de Limpeza'),
    ('vestuario', 'Vestuário'),
    ('bazar', 'Bazar'),
]

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    data_validade = models.DateField(null=True, blank=True)
    estoque_minimo = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} ({self.quantidade} unidades)"
