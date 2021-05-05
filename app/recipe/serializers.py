from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from core.models import Tag, Ingrediant


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id',  'name', 'user', ]
        read_only_fields = ('id',)


class IngrediantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediant
        fields = ['id',  'name']
        read_only_fields = ('id',)
