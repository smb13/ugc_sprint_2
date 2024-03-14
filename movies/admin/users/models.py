import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, login, password=None):
        if not login:
            raise ValueError("Users must have an email address")

        user = self.model(login=self.normalize_email(login))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None):
        user = self.create_user(login, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    login: str = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active: bool = models.BooleanField(default=True)
    is_admin: bool = models.BooleanField(default=False)
    first_name: str = models.CharField(max_length=255)
    last_name: str = models.CharField(max_length=255)

    USERNAME_FIELD = "login"

    objects = MyUserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return f"{self.login} {self.id}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
