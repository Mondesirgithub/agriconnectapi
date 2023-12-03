from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import *
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def allEquipements(request):
    equipements = Equipment.objects.all()
    serializer = EquipementSerializer(equipements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def allCategories(request):
    categories = EquipmentCategory.objects.all()
    serializer = EquipementCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def details_equipement(request, pk):
    equipement = Equipment.objects.get(pk=pk)
    serializer = EquipementSerializer(equipement, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def equipements_categorie(request, pk_category):
    categorie = EquipmentCategory.objects.get(pk=pk_category)
    equipements = categorie.equipement_set.all()
    serializer = EquipementSerializer(equipements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  



@api_view(['POST'])
def ajouter_au_panier(request, pk_product):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    equipment = Equipment.objects.get(pk=pk_product)

    quantite = int(request.data.get('equipement-quantity', 0))
    user = request.user
    panier, _ = Panier.objects.get_or_create(user=user)
    article, article_cree = Article.objects.get_or_create(user=user, est_commande=False, produit=equipment)

    if (equipment.stock - quantite) >= 0:
        if article_cree:
            article.quantite = quantite
            article.save()
            panier.articles.add(article)
            panier.save()
        else:
            article.quantite += quantite
            article.save()
            panier.save()

        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response({"detail": "Stock insuffisant"}, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['POST'])
def vider_panier(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    articles.delete()
    panier.save()
    return Response({'message' : 'Votre panier a bien été vidé'}, status=status.HTTP_200_OK)



