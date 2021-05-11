from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe, Ingrediant, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerialzer


RECIPE_URL = reverse('recipe:recipe-list')


def sample_ingrediant(user, name='name_ingrediant'):
    return Ingrediant.objects.create(user=user, name=name)


def detail_reciep(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def sample_tag(user, name='name_tag'):
    return Tag.objects.create(user=user, name=name)


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

    def test_retrive_recipe(self):
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

    def test_recipe_detail(self):
        recipe = simple_recipe(user=self.user)
        recipe.ingrediant.add(sample_ingrediant(user=self.user))
        recipe.tag.add(sample_tag(user=self.user))

        url = detail_reciep(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerialzer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_successful_created_not_assigned(self):
        default = {
            'title': 'Sample recipe',
            'time_minute': 10,
            'price': 5.00
        }
        res = self.client.post(RECIPE_URL, default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in default.keys():
            # getattr(x,y)=>x.y ex : recipe.title
            self.assertEqual(default[key], getattr(recipe, key))

    def test_create_recipe_with_tag(self):
        tag1 = sample_tag(user=self.user, name='tag1')
        tag2 = sample_tag(user=self.user, name='tag12')
        default = {
            'title': 'Sample recipe',
            'time_minute': 10,
            'price': 5.00,
            'tag': [tag1.id, tag2.id]
        }
        res = self.client.post(RECIPE_URL, default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        tags = Tag.objects.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingrediant(self):
        ingrediant1 = sample_ingrediant(user=self.user, name='tag1')
        ingrediant2 = sample_ingrediant(user=self.user, name='tag12')
        default = {
            'title': 'Sample recipe',
            'time_minute': 10,
            'price': 5.00,
            'ingrediant': [ingrediant1.id, ingrediant2.id]
        }
        res = self.client.post(RECIPE_URL, default)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        ingrediants = Ingrediant.objects.all()
        self.assertEqual(ingrediants.count(), 2)
        self.assertIn(ingrediant1, ingrediants)
        self.assertIn(ingrediant2, ingrediants)
