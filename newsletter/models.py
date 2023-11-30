from django.conf import settings
from django.db import models

from service_client.models import Client, NULLABLE


class MailingSettings(models.Model):
    """
    Модель для настроек рассылки
    """
    send_time = models.DateTimeField(verbose_name='время рассылки')

    frequency_choices = [
        ('Daily', 'Раз в день'),
        ('Weekly', 'Раз в неделю'),
        ('Monthly', 'Раз в месяц'),
    ]
    frequency = models.CharField(max_length=30, choices=frequency_choices, verbose_name='периодичность')

    status_choices = [
        ('Created', 'Создана'),
        ('Started', 'Запущена'),
        ('Completed', 'Завершена'),
    ]
    status = models.CharField(max_length=30, choices=status_choices, verbose_name='статус рассылки')

    def __str__(self):
        return f'{self.send_time} - {self.frequency}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Message(models.Model):
    """
    Модель самой рассылки с содержимым
    """
    client = models.ManyToManyField(Client, verbose_name='клиент')
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, null=True, verbose_name='настройки')

    title = models.CharField(max_length=255, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLogs(models.Model):
    """
    Модель для логов рассылки
    """
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, verbose_name='рассылка')
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=30, verbose_name='статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        return f'{self.status} в {self.datetime_attempt}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
