from django.db import models
from django.contrib.auth.models import User


class Chuva(models.Model):
    id = models.IntegerField().primary_key
    milimetros = models.IntegerField()
    data = models.DateField()
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)

    
