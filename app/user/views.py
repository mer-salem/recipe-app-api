from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import SerializerUser, AuthTokenSerializer
from rest_framework import generics
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
# Create your views here.


class ViewSerializerUser(generics.CreateAPIView):
    serializer_class = SerializerUser


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
