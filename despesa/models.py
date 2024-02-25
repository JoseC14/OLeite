from django.db import models
from django.contrib.auth.models import User


class Despesa(models.Model):
    id = models.IntegerField().primary_key
    tipo = models.CharField(max_length=100)
    gasto = models.DecimalField(max_digits=10,decimal_places=2)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)


