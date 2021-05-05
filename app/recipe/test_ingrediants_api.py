from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingrediant
from recipe.serializers import TagSerializer, IngrediantSerializer


INGREDIANT_URL = reverse('recipe:ingrediant-list')


class PublicIngrediantTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIANT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngrediantTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'ingrediant@gmail.com', 'password')
        self.client.force_authenticate(self.user)

    def test_retrive_ingrediant(self):
        Ingrediant.objects.create(user=self.user, name='cucumber')
        Ingrediant.objects.create(user=self.user, name='cucumber2')

        res = self.client.get(INGREDIANT_URL)

        ingrediant = Ingrediant.objects.all().order_by('-name')
        serializer = IngrediantSerializer(ingrediant, many=True)

        self.assertEqual(res.data, serializer.data)

    def test_ingrediant_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'ingrediant2@gmail.com', 'password2')
        ingrediant = Ingrediant.objects.create(user=self.user, name='cucumber')
        Ingrediant.objects.create(user=user2, name='cucumber2')
        res = self.client.get(INGREDIANT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK, msg=None)

        self.assertEqual(len(res.data), 1, msg=None)
        self.assertEqual(res.data[0]['name'], ingrediant.name)

    def test_create_successful_ingrediant(self):
        pyload = {'name': 'test_ingrediant'}
        res = self.client.post(INGREDIANT_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Ingrediant.objects.filter(
            user=self.user, name=pyload['name']).exists()
        self.assertTrue(exists)

    def test_create_invalid_ingrediant(self):
        pyload = {'name': ''}
        res = self.client.post(INGREDIANT_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
