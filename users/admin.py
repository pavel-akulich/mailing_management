from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для админки пользователей"""
    list_display = ('pk', 'email', 'phone', 'is_active',)
