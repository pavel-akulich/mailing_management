from django.contrib.auth.models import AbstractUser
from django.db import models

from service_client.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')

    avatar = models.ImageField(upload_to='users_avatar/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    verify_code = models.CharField(default=0, verbose_name='код верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
