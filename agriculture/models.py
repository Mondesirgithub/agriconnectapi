from django.db import models
from comptes.models import Utilisateur
from django.conf import settings
from datetime import datetime


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="agriculture/EquipmentCategory")
    
    def __str__(self):
        return self.name
    
class EquipmentSubcategory(models.Model):
    category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='owned_equipment')
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)

    nom = models.CharField(max_length=128, blank=False)
    prix = models.FloatField(default=0.0)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=128)
    stock = models.IntegerField(default=1)
    categorie = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='agriculture/equipements', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.nom} ({self.stock} en stock)")


class Rental(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)


    
class Article(models.Model):
    produit = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    est_commande = models.BooleanField(default=False)
    date_commande = models.DateTimeField(blank=True, null=True)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.produit.nom} ({self.quantite})"



class Contract(models.Model):
    TYPES = [
        ('location', 'location'),
        ('vente', 'vente'),
    ]
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='contracts')
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='signed_contracts')
    terms_and_conditions = models.TextField()
    contract_type = models.CharField(max_length=50, choices=TYPES, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Panier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return f"Panier pour {self.user.username}"


    def delete(self, *args, **kwargs):
        for article in self.articles.all():
            article.est_commande = True
            article.date_commande = datetime.now()
            article.save()

        self.articles.clear()

        super().delete(*args, **kwargs)