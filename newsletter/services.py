import os

from django.core.mail import send_mail
from newsletter.models import Message, MailingLogs
from datetime import datetime, timedelta


def send_newsletter():
    """
    Function for automatically sending messages according to the mailing settings.

    Returns:
        None
    """
    # Getting all available messages
    messages = Message.objects.all()

    # Getting the date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    messages_to_update = []

    for message in messages:
        if message.mailing_settings.send_time.time() <= current_time and message.mailing_settings.send_time.date() == current_date:

            subject = message.title
            message_body = message.body
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient_list = [client.email for client in message.client.all()]

            try:
                send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)

                # Add message to the list to update after sending
                messages_to_update.append(message)

                # Save the log entry after successful sending
                MailingLogs.objects.create(
                    message=message,
                    status='Successfully sent',
                    server_response='The newsletter has been sent successfully'
                )
            except Exception as e:
                MailingLogs.objects.create(
                    message=message,
                    status='Sending error',
                    server_response=str(e)
                )

    # Updating the sending time for the next mailing
    for message in messages_to_update:
        if message.mailing_settings.frequency == 'Daily':
            message.mailing_settings.send_time += timedelta(days=1)
        elif message.mailing_settings.frequency == 'Weekly':
            message.mailing_settings.send_time += timedelta(weeks=1)
        elif message.mailing_settings.frequency == 'Monthly':
            message.mailing_settings.send_time += timedelta(days=30)
        message.mailing_settings.save()
