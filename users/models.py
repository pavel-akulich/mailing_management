from django.contrib.auth.models import AbstractUser
from django.db import models

from service_client.models import NULLABLE


class User(AbstractUser):
    """
    Custom user model representing a user of the system.

    Attributes:
        email (EmailField): The email address of the user.
        avatar (ImageField): The avatar image of the user.
        phone (CharField): The phone number of the user.
        country (CharField): The country of the user.
        verify_code (CharField): The verification code of the user.
    """
    username = None

    email = models.EmailField(unique=True, verbose_name='email')

    avatar = models.ImageField(upload_to='users_avatar/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=40, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)

    verify_code = models.CharField(default=0, verbose_name='код верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
