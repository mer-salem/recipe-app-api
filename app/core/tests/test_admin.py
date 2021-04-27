from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='omar2@gamil.com', password='123')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='usert@gmail.com', password='456', name='aucune ide ')

    def test_users_listed(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        #print(res.json, self.user.name)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200, msg=None)

    def test_user_change_add(self):
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
