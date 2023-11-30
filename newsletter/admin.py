from django.contrib import admin

from newsletter.models import MailingSettings, Message, MailingLogs


@admin.register(MailingSettings)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'send_time', 'frequency', 'status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'mailing_settings', 'title', 'body',)


@admin.register(MailingLogs)
class MailingLogsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'message', 'datetime_attempt', 'status', 'server_response',)


