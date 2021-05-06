from django.db import models
from django.contrib.auth.models import BaseUserManager, \
    AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import Settings

from django.conf import settings

# Create your models here.


class UserModelmanager(BaseUserManager):
    def create_user(self, email, password=None, **extrat_fields):
        if not email:
            raise ValueError('user must have a email adress')
        email = self.normalize_email(email)
        user = self.model(email=email, **extrat_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extrat_fields):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserModelmanager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingrediant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    time_minute = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingrediant = models.ManyToManyField('Ingrediant')
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title
