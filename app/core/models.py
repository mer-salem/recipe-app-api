from django.db import models
from django.contrib.auth.models import BaseUserManager, \
    AbstractBaseUser, PermissionsMixin


# Create your models here.

class UserModelmanager(BaseUserManager):
    def create_user(self, email, password=None, **extrat_fields):
        if not email:
            raise ValueError('user must have a email adress')
        email = self.normalize_email(email)
        user = self.model(email=email, **extrat_fields)
        user.set_password(password)
        user.save(self._db)
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
