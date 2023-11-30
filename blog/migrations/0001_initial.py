# Generated by Django 4.2.6 on 2023-11-28 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='заголовок')),
                ('content', models.TextField(verbose_name='содержимое статьи')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='articles/', verbose_name='превью')),
                ('views_count', models.IntegerField(default=0, verbose_name='просмотры')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания публикации')),
            ],
            options={
                'verbose_name': 'статья',
                'verbose_name_plural': 'статьи',
            },
        ),
    ]