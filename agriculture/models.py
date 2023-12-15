from django.db import models
from comptes.models import Utilisateur
from django.conf import settings
from datetime import datetime


class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="agriculture/EquipmentCategory")
    
    def __str__(self):
        return self.name
    

    
class Equipment(models.Model):
    PAYMENT_CHOICES = [
        ('jour', 'Par jour'),
        ('mois', 'Par mois'),
        ('semaine', 'Par semaine'),
        # Ajoutez d'autres options selon vos besoins
    ]

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    price = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True)
    stock = models.IntegerField(blank=True, null=True)
    categorie = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='agriculture/equipements', blank=True, null=True)
    is_rented = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    rental_start_date = models.DateField(blank=True, null=True)
    rental_end_date = models.DateField(blank=True, null=True)
    rental_amount = models.FloatField(blank=True, null=True)
    rental_stock = models.IntegerField(blank=True, null=True)
    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='mois',  # Vous pouvez définir la valeur par défaut selon vos préférences
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='owned_equipment', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({'En location seulement' if self.is_rented else 'En vente seulement' if self.is_sent else 'En location + En vente ' if self.is_rented and self.is_sent else ''} - {self.stock if self.stock else 0} en stock pour la vente, {self.rental_stock if self.rental_stock else 0} en stock pour la location)"


class Rental(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    renter = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)


    
class Article(models.Model):
    equipement = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    est_commande = models.BooleanField(default=False)
    date_commande = models.DateTimeField(blank=True, null=True)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.equipement.name} ({self.quantite}) - pour {self.user.username}"


class ArticleLocation(models.Model):
    equipement = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    est_commande = models.BooleanField(default=False)
    date_commande = models.DateTimeField(blank=True, null=True)
    quantite = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.equipement.name} ({self.quantite}) - pour {self.user.username}"


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


class PanierLocation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    articles = models.ManyToManyField(ArticleLocation)

    def __str__(self):
        return f"Panier de location pour {self.user.username}"


    def delete(self, *args, **kwargs):
        for article in self.articles.all():
            article.est_commande = True
            article.date_commande = datetime.now()
            article.save()

        self.articles.clear()

        super().delete(*args, **kwargs)



