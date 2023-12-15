from django.urls import path
from . import views

urlpatterns = [
    path('details_equipement/<str:pk>', views.details_equipement, name='details_equipement'),
    path('ajouter_au_panier/<str:pk_product>', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('ajouter_au_panier_location/<str:pk_product>', views.ajouter_au_panier_location, name='ajouter_au_panier_location'),
    
    path('supprimer_au_panier/<str:pk_product>', views.supprimer_au_panier, name='supprimer_au_panier'),
    path('supprimer_au_panier_location/<str:pk_product>', views.supprimer_au_panier_location, name='supprimer_au_panier_location'),

    path('retirer_produit/<str:pk_product>', views.retirer_produit, name='retirer_produit'),
    path('retirer_produit_location/<str:pk_product>', views.retirer_produit_location, name='retirer_produit_location'),

    path('equipements_categorie/<str:pk_category>/', views.equipements_categorie, name='equipements_categorie'),
    path('vider_panier/', views.vider_panier, name='vider_panier'),
    path('vider_panier_location/', views.vider_panier_location, name='vider_panier_location'),
    path('categories/', views.allCategories, name='categories'),

    path('articles/', views.allArticles, name='articles'),
    path('articles_location/', views.allArticlesLocation, name='articles_location'),

    path('checkout/', views.checkout, name='checkout'),



    path('equipements/', views.allEquipements, name='equipements'),
    path('equipementsUser/', views.allEquipementsUser, name='equipements'),
    path('rent_equipement/<str:pk>', views.rent_equipement, name='rent_equipement'),
    path('unrent_equipement/<str:pk>', views.unrent_equipement, name='unrent_equipement'),
    path('callback/', views.callback, name='callback'),
    

    path('sent_equipement/<str:pk>', views.sent_equipement, name='sent_equipement'),
    path('unsent_equipement/<str:pk>', views.unsent_equipement, name='unsent_equipement'),
    path('register_equipement/', views.register_equipement, name='register_equipement'),
]