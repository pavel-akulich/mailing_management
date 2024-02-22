from django.conf import settings
from django.db import models

from service_client.models import Client, NULLABLE


class MailingSettings(models.Model):
    """
    Model for managing mailing settings.

    Attributes:
        send_time (DateTimeField): Date and time for sending the mailing.
        frequency (CharField): Frequency of the mailing (choices: Daily, Weekly, Monthly).
        status (CharField): Status of the mailing (choices: Created, Started, Completed).
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
        """
        String representation of the object.
        """
        return f'{self.send_time} - {self.frequency}'

    class Meta:
        """
        Meta_class settings for the MailingSettings model.
        """
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Message(models.Model):
    """
    Model for managing messages and their content.

    Attributes:
        client (ManyToManyField): Clients associated with the message.
        mailing_settings (ForeignKey): Mailing settings associated with the message.
        title (CharField): Title of the message.
        body (TextField): Body/content of the message.
        owner (ForeignKey): Owner of the message (linked to settings.AUTH_USER_MODEL).
        is_active (BooleanField): Flag indicating if the message is active or not.
    """
    client = models.ManyToManyField(Client, verbose_name='клиент')
    mailing_settings = models.ForeignKey(MailingSettings, on_delete=models.SET_NULL, null=True,
                                         verbose_name='настройки')

    title = models.CharField(max_length=255, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец')
    is_active = models.BooleanField(default=True, verbose_name='признак активности')

    def __str__(self):
        """
        String representation of the object.
        """
        return self.title

    class Meta:
        """
        Meta_class settings for the Message model.
        """
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLogs(models.Model):
    """
    Model for managing mailing logs.

    Attributes:
        message (ForeignKey): Message associated with the log.
        datetime_attempt (DateTimeField): Date and time of the mailing attempt.
        status (CharField): Status of the mailing attempt.
        server_response (TextField): Server response for the mailing attempt.
    """
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, verbose_name='рассылка')
    datetime_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=30, verbose_name='статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='ответ почтового сервера')

    def __str__(self):
        """
        String representation of the object.
        """
        return f'{self.status} в {self.datetime_attempt}'

    class Meta:
        """
        Meta_class settings for the MailingLogs model.
        """
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
