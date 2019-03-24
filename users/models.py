from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import PermissionsMixin

from django.shortcuts import get_object_or_404

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_admin=False):
        if not email:
            raise ValueError('Email is required!')
        if not password:
            raise ValueError('Enter a password!')
        if not username:
            raise ValueError('Username is required!')

        user_obj = self.model(
            email = self.normalize_email(email),
            username = username
            )

        user_obj.set_password(password)
        user_obj.username = username
        user_obj.is_admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
                username,
                email,
                password = password,
                is_admin = True,
            )
        return user

    def validate(self, data):
        email = data['email']
        user_qs = Users.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError('This Email Adress already exists!')
        return data

class Users(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)
    year_of_birth = models.IntegerField(blank=True, null=True)
    language = models.CharField(max_length=32, blank=True, null=True)
    verified = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        managed = False
        db_table = 'users'

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    