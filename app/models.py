from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model):
    id = models.IntegerField().primary_key
    tipo_agricultor = models.CharField(max_length=100)
    cidade = models.CharField(max_length=200)
    estado = models.CharField(max_length=100)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)