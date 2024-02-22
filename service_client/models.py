from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Model representing a client of the service.

    Attributes:
        first_name (CharField): The first name of the client.
        last_name (CharField): The last name of the client.
        patronymic (CharField): The patronymic of the client.
        email (EmailField): The email address of the client.
        comment (TextField): Additional comment about the client.
    """
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    patronymic = models.CharField(**NULLABLE, max_length=100, verbose_name='отчество')
    email = models.EmailField(unique=True, max_length=255, verbose_name='почта клиента')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        """
        String representation of the client object.
        """
        return f'Клиент {self.first_name} с почтой {self.email}'

    class Meta:
        """
        Meta_class configuration for the Client model.
        """
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
