from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Utilisateur(AbstractUser):
    photo = models.ImageField(upload_to="comptes/utilisateurs", null=True, blank=True, default="photos/comptes/my_profile.png")
    adresse = models.CharField(max_length=50, blank=True, null=True)
    telephone = models.CharField(max_length=50, blank=True, null=True)
    culture = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.email}"