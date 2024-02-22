import os

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from newsletter.models import Message, MailingLogs


class Command(BaseCommand):
    """
    Command to manually execute mailing from the terminal.
    """
    help = 'Send all messages'

    def handle(self, *args, **options):
        """
        Handle method for executing the command.

        Args:
            *args: Additional arguments.
            **options: Additional options.

        Returns:
            None
        """
        # Get all available messages (mailings)
        messages = Message.objects.all()

        for message in messages:
            # Define parameters for sending the message
            subject = message.title
            message_body = message.body
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient_list = [client.email for client in message.client.all()]

            try:
                # Sending a message
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                # Create and save a log entry after successful submission
                MailingLogs.objects.create(
                    message=message,
                    status='Successfully sent',
                    server_response='The newsletter has been sent successfully'
                )

                self.stdout.write(self.style.SUCCESS('All messages have been sent successfully'))

            except Exception as e:
                MailingLogs.objects.create(
                    message=message,
                    status='Sending error',
                    server_response=str(e)
                )
