from rest_framework.response import Response

from rest_framework import status, viewsets, filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from core.models import Tag, Ingrediant, Recipe
from recipe.serializers import TagSerializer, IngrediantSerializer, RecipeSerializer, RecipeDetailSerialzer


# viewsets.GenericViewSet,mixins.ListModelMixin


# ==viewsets.ModelViewSet
class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    FIELD_ORDERED = '-name'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id).order_by(self.FIELD_ORDERED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagView(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    FIELD_ORDERED = '-name'


class IngrediantView(BaseRecipeAttrViewSet):
    queryset = Ingrediant.objects.all()
    serializer_class = IngrediantSerializer
    FIELD_ORDERED = '-name'


class RecipeView(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RecipeDetailSerialzer
        return RecipeSerializer
