from django.db import models
from django.contrib.auth.models import User

class PassRecovery(models.Model):
    id = models.IntegerField().primary_key
    code = models.IntegerField()
    email = models.EmailField()