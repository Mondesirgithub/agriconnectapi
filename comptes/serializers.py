from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


class UtilisateurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Utilisateur
        fields = '__all__'



class UtilisateurSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    class Meta:
        model = Utilisateur
        fields = '__all__'