from django.contrib import admin

from service_client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'patronymic', 'email', )
    search_fields = ('first_name', 'email',)
