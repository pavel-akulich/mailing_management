from django.contrib import admin

from service_client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Client model.

    Attributes:
        list_display (tuple): Tuple containing the fields to be displayed in the admin list view.
        search_fields (tuple): Tuple containing the fields to be searched in the admin list view.
    """
    list_display = ('pk', 'first_name', 'last_name', 'patronymic', 'email',)
    search_fields = ('first_name', 'email',)
