from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):

        pyload = {'email': 'test@gamil.com',
                  'password': 'test133',  'name': 'test'}

        res = self.client.post(CREATE_USER_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(pyload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        pyload = {'email': 'test@gamil.com',
                  'password': 'test133',  'name': 'test'}
        create_user(**pyload)
        # print(user.password)
        # print(user.check_password('test133'))
        res = self.client.post(CREATE_USER_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        pyload = {'email': 'test@gamil.com',
                  'password': 'te', 'name': 'test'}
        res = self.client.post(CREATE_USER_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=pyload['email']).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        pyload = {'email': 'test@gamil.com',
                  'password': 'testveza'}
        create_user(**pyload)
        res = self.client.post(TOKEN_URL, pyload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def tes_token_invalide_credentials(self):
        pyload = {'email': 'test@gamil.com',
                  'password': 'testveza'}
        create_user(**pyload)
        res = self.client.post(
            TOKEN_URL, {'email': 'test@gamil.com', 'password': '123456'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_no_user(self):
        pyload = {'email': 'test@gamil.com',
                  'password': 'testveza'}
        res = self.client.post(TOKEN_URL, pyload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):
        res = self.client.post(
            TOKEN_URL, {'email': 'tcom', 'password': ''})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrive_unauthorized_user(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTests(TestCase):
    def setUp(self):
        self.user = create_user(email='test@gmail.com',
                                password='testtest', name='name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_success_retrive_profile(self):
        res = self.client.get(ME_URL)
        print(self.user.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {'email': self.user.email, 'name': self.user.name})

    def test_post_method_not_allowed(self):
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_method(self):
        pyload = {'password': 'test_up', 'name': 'name_up'}
        res = self.client.patch(ME_URL, pyload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, pyload['name'])
        self.assertTrue(self.user.check_password(pyload['password']))
