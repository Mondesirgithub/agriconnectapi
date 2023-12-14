from comptes.models import *
from comptes.serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Utilisateur
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from comptes.models import *
from comptes.serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from django.utils.html import strip_tags
from django.shortcuts import get_object_or_404
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)        
            user = Utilisateur.objects.filter(username=attrs['username']).first()

            if user and user.check_password(attrs['password']):
                serializer = UtilisateurSerializerWithToken(user).data
                for k, v in serializer.items():
                    data[k] = v
                return data

        except:
            return {'message':'username et/ou mot de passe incorrect'}
         
class MyTokenObtainPairViews(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def users(request, pk=None):
    if pk is None:
        users = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(users, many=True)
        return Response(serializer.data)
    else:
        try:
            user = Utilisateur.objects.get(pk=pk)
            serializer = UtilisateurSerializer(user, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            message = {'message' : 'user inexistant'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)  
        except:
            message = {'message' : 'Un problème est survenu !, veuillez réessayer'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)    
        


@api_view(['POST'])
def registerUser(request):
    data = request.data

    user = Utilisateur.objects.create(
        last_name = data['nom'],
        first_name = data['prenom'],
        adresse = data['adresse'],
        telephone = data['telephone'],
        culture = data['culture'],
        username = data['username'],
        password = make_password(data['password'])
    )
    serializer = UtilisateurSerializerWithToken(user, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
def updateUser(request , id):
    data = request.data

    try:
        user = Utilisateur.objects.get(id=id)

        if user.last_name != data['last_name']:
            if Utilisateur.objects.filter(last_name=data['last_name']).exists():
                message = {'message' : 'Un utilisateur avec ce nom existe déjà'}
                return Response(message)
        
        if user.email != data['email']:
            if Utilisateur.objects.filter(email=data['email']).exists():
                return Response({'message': 'Un utilisateur avec cette adresse e-mail existe déjà, veuillez la changer'}, status=status.HTTP_400_BAD_REQUEST)


        if user.telephone != data['telephone']:
            if data['telephone'] != '' and Utilisateur.objects.filter(telephone=data['telephone']).exists():
                return Response({'message': 'Un utilisateur avec ce numéro de téléphone existe déjà, veuillez le changer'}, status=status.HTTP_400_BAD_REQUEST)


        # Mettez à jour les champs appropriés du professeur
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.telephone = data['telephone']
        user.adresse = data['adresse']

        # Renvoyez les données mises à jour si nécessaire
        serializer = UtilisateurSerializerWithToken(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Utilisateur.DoesNotExist:
        return Response({'message': 'L\'utilisateur spécifié n\'existe pas'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': f'Une erreur s\'est produite lors de la mise à jour du professeur : {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def get_user_photo(request, id):
    user = get_object_or_404(Utilisateur, id=id)
    if user.photo:
        photo_url = user.photo.url
        return Response({'photo_url': photo_url}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'L\'utilisateur n\'a pas de photo'}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['PUT'])
def update_user_photo(request, id):
    user = get_object_or_404(Utilisateur, id=id)
    if 'photo' in request.data:
        user.photo = request.data['photo']
        user.save()
        sserializer = UtilisateurSerializerWithToken(user, many=False)
        return Response(sserializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Aucune photo n\'a été fournie'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def change_password(request):
    email = request.data["email"]
    try:
        user = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Aucun utilisateur trouvé avec cette adresse e-mail'}, status=status.HTTP_400_BAD_REQUEST)
    
    new_password = request.data.get('new_password')
    
    # Vérifier que le nouveau mot de passe est valide
    if not new_password or len(new_password) < 6:
        return Response({'error': 'Le nouveau mot de passe doit contenir au moins 6 caractères'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Changer le mot de passe
    user.set_password(new_password)
    user.save()
    
    return Response({'success': 'Mot de passe modifié avec succès'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def envoyer_mail(request):
    email = request.data["email"]
    try:
        user = Utilisateur.objects.get(email=email)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Aucun utilisateur trouvé avec cette adresse e-mail'}, status=status.HTTP_400_BAD_REQUEST)
    
    subject = "Réinitialisation du mot de passe"
    template = 'comptes/email_reset_password.html'
    context = {'user': user}
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)  # Version texte brut du message
    recipient_list = [user.email]
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message)   
    
    return Response({'success': 'Nous vous avons envoyer un message, vérifiez votre boîte mail 😊!'}, status=status.HTTP_200_OK)             
    