from django.db import models

from service_client.models import NULLABLE


class Blog(models.Model):
    """
        Model for managing blog posts.

    Attributes:
        title (CharField): Title of the blog post.
        content (TextField): Content of the blog post.
        preview (ImageField): Image preview of the blog post.
        views_count (IntegerField): Number of views for the blog post.
        created_at (DateTimeField): Date and time when the blog post was created.
    """
    title = models.CharField(max_length=255, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')
    preview = models.ImageField(**NULLABLE, upload_to='articles/', verbose_name='превью')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания публикации')

    def __str__(self):
        """
        String representation of the object.
        """
        return f'{self.title}'

    class Meta:
        """
        Class Meta settings for objects.
        """
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
