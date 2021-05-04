from rest_framework.response import Response

from rest_framework import status, viewsets, filters, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from core.models import Tag
from recipe.serializers import TagSerializer


class TagView(viewsets.ModelViewSet):  # viewsets.GenericViewSet,mixins.ListModelMixin
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user.id).order_by('-name')

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
