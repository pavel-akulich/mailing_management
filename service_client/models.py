from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """Модель для клиента сервиса"""
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    patronymic = models.CharField(**NULLABLE, max_length=100, verbose_name='отчество')
    email = models.EmailField(max_length=255, verbose_name='почта клиента')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return f'Клиент {self.first_name} с почтой {self.email}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
