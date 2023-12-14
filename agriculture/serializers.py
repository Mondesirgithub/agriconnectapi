from rest_framework import serializers
from .models import *
from .serializers import *

class UtilisateurSerializer(serializers.ModelSerializer):
    # Ajoutez des champs supplémentaires au besoin

    class Meta:
        model = Utilisateur
        fields = '__all__'

class EquipementCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentCategory
        fields = '__all__'

class EquipementSerializer(serializers.ModelSerializer):
    categorie = EquipementCategorySerializer()
    owner = UtilisateurSerializer()
    
    class Meta:
        model = Equipment
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    equipement = EquipementSerializer()
    class Meta:
        model = Article
        fields = '__all__'


class ArticleLocationSerializer(serializers.ModelSerializer):
    equipement = EquipementSerializer()
    class Meta:
        model = ArticleLocation
        fields = '__all__'


class PanierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Panier
        fields = '__all__'


class PanierLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = PanierLocation
        fields = '__all__'