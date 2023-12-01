from django.db import models

from service_client.models import NULLABLE


class Blog(models.Model):
    """
    Модель для ведения блога
    """
    title = models.CharField(max_length=255, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи')
    preview = models.ImageField(**NULLABLE, upload_to='articles/', verbose_name='превью')
    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания публикации')

    def __str__(self):
        """Строковое представление объекта"""
        return f'{self.title}'

    class Meta:
        """Мета класс настройка для объектов"""
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


