from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Blog model.

    Attributes:
        list_display (tuple): Tuple containing the fields to be displayed in the admin list view.
    """
    list_display = ('pk', 'title', 'views_count', 'created_at',)
