from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Gado(models.Model):
    id = models.IntegerField().primary_key
    nome = models.CharField(max_length=150, unique=True)
    leitera = models.BooleanField()
    tipo = models.CharField(max_length=50)
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

