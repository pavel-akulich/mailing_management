from django.contrib import admin

from newsletter.models import MailingSettings, Message, MailingLogs


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MailingSettings model.

    Attributes:
        list_display (tuple): Tuple containing the fields to be displayed in the admin list view.
    """
    list_display = ('pk', 'send_time', 'frequency', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Message model.

    Attributes:
        list_display (tuple): Tuple containing the fields to be displayed in the admin list view.
    """
    list_display = ('pk', 'mailing_settings', 'title', 'body',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    """
    Admin configuration for the MailingLogs model.

    Attributes:
        list_display (tuple): Tuple containing the fields to be displayed in the admin list view.
    """
    list_display = ('pk', 'message', 'datetime_attempt', 'status', 'server_response',)
