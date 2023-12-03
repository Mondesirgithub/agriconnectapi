from django.urls import path
from . import views

urlpatterns = [
    path('details_equipement/<str:pk>', views.details_equipement, name='details_equipement'),
    path('ajouter_au_panier/<str:pk_product>', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('equipements_categorie/<int:pk_category>', views.equipements_categorie, name='equipements_categorie'),
    path('vider_panier/', views.vider_panier, name='vider_panier'),
    path('categories/', views.allCategories, name='categories'),
    path('equipements/', views.allEquipements, name='equipements'),
]