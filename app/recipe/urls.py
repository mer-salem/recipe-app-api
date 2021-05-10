from django.urls import path, include

from rest_framework.routers import DefaultRouter
from recipe.views import TagView, IngrediantView, RecipeView

router = DefaultRouter()

router.register('tags', TagView)
router.register('ingrediants', IngrediantView)
router.register('recipes', RecipeView)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
