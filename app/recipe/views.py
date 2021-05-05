from rest_framework.response import Response

from rest_framework import status, viewsets, filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from core.models import Tag, Ingrediant
from recipe.serializers import TagSerializer, IngrediantSerializer


# viewsets.GenericViewSet,mixins.ListModelMixin
class TagView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IngrediantView(viewsets.ModelViewSet):
    queryset = Ingrediant.objects.all()
    serializer_class = IngrediantSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
