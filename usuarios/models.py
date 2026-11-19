# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    codigo_uncp = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username}"