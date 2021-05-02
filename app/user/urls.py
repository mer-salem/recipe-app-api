from django.urls import path, include
from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

#router.register('me', views.ViewUpdateUser, basename='me')

app_name = 'user'
urlpatterns = [
    path('create/', views.ViewSerializerUser.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    #url('', include(router.urls)),
    url('me/', views.ViewUpdateUser.as_view(), name='me'),
]
