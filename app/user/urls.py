from django.urls import path, include
from django.conf.urls import url
from . import views


app_name = 'user'
urlpatterns = [
    path('create/', views.ViewSerializerUser.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    url('me/', views.ViewUpdateUser.as_view(), name='me'),
]
