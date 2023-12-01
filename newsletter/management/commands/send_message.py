from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from newsletter.models import Message, MailingLogs


class Command(BaseCommand):
    """
    Команда для выполнения рассылки в ручную из терминала
    """
    help = 'Отправить все сообщения'

    def handle(self, *args, **options):
        # Получаем все доступные сообщения(рассылки)
        messages = Message.objects.all()

        for message in messages:
            # Определяем параметры для отправки сообщения
            subject = message.title
            message_body = message.body
            from_email = 'noreplyservice1@mail.ru'  # Почта с которой улетит рассылка
            recipient_list = [client.email for client in message.client.all()]

            try:
                # Отправляем сообщение
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                # Создаем и сохраняем запись лога после успешной отправки
                MailingLogs.objects.create(
                    message=message,
                    status='Успешно отправлено',
                    server_response='Рассылка успешно отправлена'
                )

                self.stdout.write(self.style.SUCCESS('Все сообщения успешно отправлены'))

            except Exception as e:
                # Если отправка не удалась, создаем запись лога с информацией об ошибке
                MailingLogs.objects.create(
                    message=message,
                    status='Ошибка отправки',
                    server_response=str(e)
                )

