from django.urls import path, include

from rest_framework.routers import DefaultRouter
from recipe.views import TagView

router = DefaultRouter()

router.register('tags', TagView, basename='tag')
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
