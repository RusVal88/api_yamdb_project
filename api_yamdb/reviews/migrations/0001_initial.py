# Generated by Django 3.2 on 2023-03-23 21:09

import api.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название категории', max_length=256, verbose_name='Категория')),
                ('slug', models.SlugField(help_text='Введите адрес категории', unique=True, verbose_name='Страница категории')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Напишите ваш комментарий', verbose_name='Комментарий')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название жанра', max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(help_text='Введите адрес страницы жанра,', unique=True, verbose_name='Страница жанра')),
            ],
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(help_text='Введите заголовок обзора', max_length=256, verbose_name='Заголовок')),
                ('text', models.TextField(help_text='Напишите обзор', verbose_name='Текст')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('score', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], help_text='Выберите оценку от 1 до 10', verbose_name='Оценка')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, help_text='О чем данное произведение?', null=True, verbose_name='Описание произведения')),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рейтинг')),
                ('year', models.IntegerField(db_index=True, help_text='Укажите год создания произведения', validators=[api.validators.validate_year], verbose_name='Год создания')),
                ('name', models.CharField(help_text='Введите название произведения', max_length=256, verbose_name='Произведение')),
                ('category', models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(help_text='Выберите жанр', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='Жанр')),
            ],
        ),
    ]
