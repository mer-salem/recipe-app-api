from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsTests(TestCase):
    def setUp(self):
        self.email = 'test@gmail.com'
        self.password = 'password'
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(self.email, self.password)
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        Tag.objects.create(user=self.user, name='vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tag = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tag, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        self.user2 = get_user_model().objects.create_user('test2@gmail.com', 'password2')
        Tag.objects.create(user=self.user2, name='vegan')
        tag = Tag.objects.create(user=self.user, name='Dessert')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_successful_tag(self):

        pyload = {'user': self.user, 'name': 'tag'}
        res = self.client.post(TAGS_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        exists = Tag.objects.filter(name=pyload['name']).exists()
        self.assertTrue(exists)

    def test_valide_tag_error(self):

        pyload = {'name': ''}
        res = self.client.post(TAGS_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
