from rest_framework import serializers
from .models import *
from .serializers import *


class EquipementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = '__all__'


class EquipementCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EquipmentCategory
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'