from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import SerializerUser, AuthTokenSerializer
from rest_framework import generics, mixins, viewsets
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.http import require_http_methods
# Create your views here.
from core.models import Me


class ViewSerializerUser(generics.CreateAPIView):
    serializer_class = SerializerUser


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# @require_http_methods(["GET", "POST"])
class ViewUpdateUser(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # queryset = get_user_model().objects.all()
    serializer_class = SerializerUser
    #lookup_field = 'id'

    def get_object(self):
        return self.request.user
