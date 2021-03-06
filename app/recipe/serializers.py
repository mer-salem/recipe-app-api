from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from core.models import Tag, Ingrediant, Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id',  'name', 'user', ]
        read_only_fields = ('id', 'user')


class IngrediantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediant
        fields = ['id',  'name']
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    ingrediant = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingrediant.objects.all())
    tag = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ['id', 'user',  'title',
                  'time_minute', 'price', 'ingrediant', 'tag', 'link']
        read_only_fields = ('id', 'user',)


class RecipeDetailSerialzer(RecipeSerializer):

    ingrediant = IngrediantSerializer(many=True, read_only=True)
    tag = TagSerializer(many=True, read_only=True)
