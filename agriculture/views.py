from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
# Create your views here.
from .utils.functions import genererate_string, process_phone_number_cg_am

@api_view(['GET'])
def allEquipements(request):
    equipements = Equipment.objects.all()
    serializer = EquipementSerializer(equipements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['PUT'])
def rent_equipement(request, pk):
    try:
        equipement = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response({"detail": "L'équipement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data

    # Mettez à jour les champs appropriés de l'équipement
    equipement.is_rented = True
    equipement.rental_start_date = data.get('startDate')
    equipement.rental_end_date = data.get('endDate')
    equipement.rental_stock = data.get('stock')
    equipement.rental_amount = data.get('amount')
    equipement.payment_mode = data.get('paymentMode')


    # Enregistrez les modifications
    equipement.save()

    return Response({"detail": "L'équipement est disponible en location"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def sent_equipement(request, pk):
    try:
        equipement = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response({"detail": "L'équipement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
    data = request.data
    # Mettez à jour les champs appropriés de l'équipement
    equipement.is_sent = True
    equipement.price = data['price']
    equipement.stock = data['stock']
    # Enregistrez les modifications
    equipement.save()

    return Response({"detail": "L'équipement est disponible en location"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def unrent_equipement(request, pk):
    try:
        equipement = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response({"detail": "L'équipement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    # if request.method == 'PUT':
    #     # Assurez-vous que l'utilisateur connecté est le propriétaire de l'équipement
    #     if equipement.owner != request.user:
    #         return Response({"detail": "Vous n'êtes pas autorisé à mettre à jour cet équipement"}, status=status.HTTP_403_FORBIDDEN)

    # Récupérez les données mises à jour depuis la requête
    # Mettez à jour les champs appropriés de l'équipement
    equipement.is_rented = False
    equipement.rental_start_date = None
    equipement.rental_end_date = None
    equipement.rental_stock = None
    equipement.rental_amount = None

    # Enregistrez les modifications
    equipement.save()

    return Response({"detail": "L'équipement n'est pas disponible en vente"}, status=status.HTTP_200_OK)

@api_view(['PUT'])
def unsent_equipement(request, pk):
    try:
        equipement = Equipment.objects.get(pk=pk)
    except Equipment.DoesNotExist:
        return Response({"detail": "L'équipement n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

    equipement.is_sent = False
    equipement.price = None,
    equipement.stock = None,
    # Enregistrez les modifications
    equipement.save()

    return Response({"detail": "L'équipement n'est pas disponible en vente"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_equipement(request):
    data=request.data
    try:
        categorie = EquipmentCategory.objects.get(pk=data['categorie'])
        equipement = Equipment.objects.create(
            name = data['name'],
            description = data['description'],
            address = data['address'],
            image = data['image'],
            categorie = categorie,
            owner=request.user
        )
        serializer = EquipementSerializer(equipement, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(f"Message : {e}")
        return Response({"message" : f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def allCategories(request):
    categories = EquipmentCategory.objects.all()
    serializer = EquipementCategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  


@api_view(['POST'])
def checkout(request):
    data = request.data
    try:
        api_url = "https://www.tstcgb.com/postswitch/epay000.php/"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "merchantID": "MOKO-PAY-CG",
            "merchantPWD": "mKP@081123100702@",
            "transID": genererate_string(),
            "amount": 50,
            "msisdn" : process_phone_number_cg_am(data['phone_number']),
            "callbackUrl":"http://apitest.mokopay.net/callback/cg_am/",
            "action": "getID"
        } 
        response = requests.post(api_url, data=data, headers=headers)
        print("===> ", response.status_code)
        return Response({"message":f"Veuillez continuer le processus sur votre téléphone portable"})
    except Exception as e:
        return Response({"error":f"Erreur survenue lors de la communication avec Airtel {e}"})


@api_view(['GET'])
def allArticles(request):
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def allArticlesLocation(request):
    articles = ArticleLocation.objects.all()
    serializer = ArticleLocationSerializer(articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def details_equipement(request, pk):
    equipement = Equipment.objects.get(pk=pk)
    serializer = EquipementSerializer(equipement, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def equipements_categorie(request, pk_category):
    categorie = EquipmentCategory.objects.get(pk=pk_category)
    equipements = categorie.equipment_set.all()
    print(equipements)
    serializer = EquipementSerializer(equipements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)  



@api_view(['POST'])
def ajouter_au_panier(request, pk_product):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    equipment = Equipment.objects.get(pk=pk_product)

    quantite = int(request.data.get('quantity', 1))
    user = request.user
    article, article_cree = Article.objects.get_or_create(user=user, est_commande=False, equipement=equipment)

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


@api_view(['POST'])
def ajouter_au_panier_location(request, pk_product):
    panier, _ = PanierLocation.objects.get_or_create(user=request.user)
    equipment = Equipment.objects.get(pk=pk_product)

    quantite = int(request.data.get('quantity', 1))
    user = request.user
    article, article_cree = ArticleLocation.objects.get_or_create(user=user, est_commande=False, equipement=equipment)

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

@api_view(['POST'])
def supprimer_au_panier(request, pk_product):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    equipment = Equipment.objects.get(pk=pk_product)

    quantite = int(request.data.get('quantity', 1))
    user = request.user
    article = Article.objects.get(user=user, equipement=equipment)

    article.quantite -= quantite
    article.save()
    panier.save()

    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def supprimer_au_panier_location(request, pk_product):
    panier, _ = PanierLocation.objects.get_or_create(user=request.user)
    equipment = Equipment.objects.get(pk=pk_product)

    quantite = int(request.data.get('quantity', 1))
    user = request.user
    article = ArticleLocation.objects.get(user=user, equipement=equipment)

    article.quantite -= quantite
    article.save()
    panier.save()

    serializer = ArticleLocationSerializer(article, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def retirer_produit(request, pk_product):
    # Obtenez le panier de l'utilisateur
    panier, _ = Panier.objects.get_or_create(user=request.user)
    
    # Obtenez l'équipement à retirer
    equipment = Equipment.objects.get(pk=pk_product)

    # Obtenez l'article lié à l'équipement dans le panier de l'utilisateur
    user = request.user
    article = Article.objects.get(user=user, produit=equipment)

    # Supprimez l'article du panier
    panier.articles.remove(article)
    panier.save()

    # Réponse indiquant que l'article a été supprimé
    return Response({"message": "L'article a été supprimé du panier"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def retirer_produit_location(request, pk_product):
    # Obtenez le panier de l'utilisateur
    panier, _ = PanierLocation.objects.get_or_create(user=request.user)
    
    # Obtenez l'équipement à retirer
    equipment = Equipment.objects.get(pk=pk_product)

    # Obtenez l'article lié à l'équipement dans le panier de l'utilisateur
    user = request.user
    article = ArticleLocation.objects.get(user=user, produit=equipment)

    # Supprimez l'article du panier
    panier.articles.remove(article)
    panier.save()

    # Réponse indiquant que l'article a été supprimé
    return Response({"message": "L'article a été supprimé du panier de location"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def vider_panier(request):
    panier, _ = Panier.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    articles.delete()
    panier.save()
    return Response({'message' : 'Votre panier a bien été vidé'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def vider_panier_location(request):
    panier, _ = PanierLocation.objects.get_or_create(user=request.user)
    articles = panier.articles.all()
    articles.delete()
    panier.save()
    return Response({'message' : 'Votre panier de location a bien été vidé'}, status=status.HTTP_200_OK)


