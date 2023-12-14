from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.ArticleLocation)
admin.site.register(models.Contract)
admin.site.register(models.Equipment)
admin.site.register(models.EquipmentCategory)
admin.site.register(models.Panier)
admin.site.register(models.PanierLocation)
admin.site.register(models.Rental)