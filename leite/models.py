from django.db import models
from django.contrib.auth.models import User
class Soma(models.Model):
    id = models.IntegerField().primary_key
    quantidade = models.IntegerField()
    preco_litro = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)


class Leite(models.Model):
    id = models.IntegerField().primary_key
    quantidade = models.IntegerField()
    data = models.DateField()
    soma = models.ForeignKey(Soma,null=True, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)