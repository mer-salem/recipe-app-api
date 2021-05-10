from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe, Ingrediant, Tag
from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse('recipe:recipe-list')


def simple_recipe(user, **params):
    default = {
        'title': 'Sample recipe',
        'time_minute': 10,
        'price': 5.00
    }
    default.update(params)
    return Recipe.objects.create(user=user, **default)


class PublicRecipeTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'recipe@gmail.com', 'password')
        self.client.force_authenticate(self.user)

    def test_retrive_ingrediant(self):
        simple_recipe(self.user)
        simple_recipe(self.user, title='recipe01')

        res = self.client.get(RECIPE_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'ingrediant2@gmail.com', 'password2')
        simple_recipe(user2)
        recipe1 = simple_recipe(self.user, title='title_test')
        res = self.client.get(RECIPE_URL)
        recipe = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipe, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=None)
        self.assertEqual(res.data, serializer.data)
        self.assertEqual(len(res.data), 1, msg=None)
        self.assertEqual(res.data[0]['title'], recipe1.title)

#     def test_create_successful_recipe(self):
#         ingrediant = Ingrediant.objects.create(
#             user=self.user, name='recipe_ingrediant')
#         tag = Tag.objects.create(user=self.user, name='recipe_tag')
#         ingrediant1 = Ingrediant.objects.all()
#         tag1 = Tag.objects.all()
#         print(ingrediant1, ingrediant)
#         pyload = {
#             'title': 'Sample recipe',
#             'time_minute': 10,
#             'price': 5,
#             'ingrediant': [ingrediant1],
#             'tag': [tag1]
#         }
#         res = self.client.post(RECIPE_URL, pyload)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         exists = Recipe.objects.filter(
#             user=self.user, title=pyload['title']).exists()
#         self.assertTrue(exists)

#     def test_create_invalid_recipe(self):
#         pyload = {'title': ''}
#         res = self.client.post(RECIPE_URL, pyload)
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
