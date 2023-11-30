from django.core.mail import send_mail
from newsletter.models import Message, MailingLogs
from datetime import datetime, timedelta


def send_newsletter():
    """
    Функция для автоматической рассылки сообщений в соответствии с настройками рассылки
    """
    # Получаем все доступные сообщения
    messages = Message.objects.all()

    # Получаем дату и время
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    for message in messages:
        if message.mailing_settings.send_time.time() <= current_time and message.mailing_settings.send_time.date() == current_date:

            # Определяем параметры для отправки сообщения
            subject = message.title
            message_body = message.body
            from_email = 'noreplyservice1@mail.ru'  # Почта(сервер) с которой улетит рассылка
            recipient_list = [client.email for client in message.client.all()]

            try:
                # Отправляем рассылку
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                # После рассылки переопределяем настройки даты, когда будет следующая рассылка
                if message.mailing_settings.frequency == 'Daily':
                    message.mailing_settings.send_time += timedelta(days=1)
                elif message.mailing_settings.frequency == 'Weekly':
                    message.mailing_settings.send_time += timedelta(days=7)
                elif message.mailing_settings.frequency == 'Monthly':
                    message.mailing_settings.send_time += timedelta(days=30)
                message.mailing_settings.save()

                # Сохраняем запись лога после успешной отправки
                MailingLogs.objects.create(
                    message=message,
                    status='Успешно отправлено',
                    server_response='Рассылка успешно отправлена'
                )
            except Exception as e:
                # Если отправка не удалась, создаем запись лога с информацией об ошибке
                MailingLogs.objects.create(
                    message=message,
                    status='Ошибка отправки',
                    server_response=str(e)
                )
