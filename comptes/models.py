from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Utilisateur(AbstractUser):
    photo = models.ImageField(upload_to="comptes/utilisateurs")