from django.test import TestCase
from django.contrib.auth import get_user_model
# from django.contrib.auth.base_user import AbstractBaseUser
from core import models


def simple_user(email='test@gmail.com', password='password'):
    return get_user_model().objects.create_user(email, password)


class TestCaseModel(TestCase):
    email = 'vezA@gmail.com'
    password = 'veza12121212'

    def test_user_create_wuth_email(self):
        email = 'vezA@gmail.com'
        password = 'veza12121212'
        user = \
            get_user_model(). \
            objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_email_normalized(self):
        email = 'veza@gmail.com'
        user = get_user_model().objects.create_user(email, '123')
        self.assertEqual(user.email, email.lower())

    def test_email_adress(self):
        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user(None, 'tset123')
            return user

    def test_is_super_user(self):
        user = get_user_model(). \
            objects.create_superuser(self.email, self.password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_staff)

    def test_get_username(self):
        email = 'veza@gmail.com'
        user = get_user_model().objects.create_user(email, '123')
        self.assertEqual(user.email, user.get_username())

    def test_tag_representation(self):
        tag = models.Tag.objects.create(user=simple_user(), name='fruits')
        self.assertEqual(str(tag), tag.name)

    def test_ingrediant_representation(self):
        ingrediant = models.Ingrediant.objects.create(
            user=simple_user(), name='Cucumber')
        self.assertEqual(str(ingrediant), ingrediant.name)

    def test_recipe_representation(self):
        recipe = models.Recipe.objects.create(
            user=simple_user(),
            title='recipe1',
            time_minute=5,
            price=5.00)
        self.assertEqual(str(recipe), recipe.title)
