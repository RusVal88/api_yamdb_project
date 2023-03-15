from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Страница категории',
        help_text='Введите адрес страницы категории, доступные символы: ^[-a-zA-Z0-9_]+$',
        unique=True,
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Жанр',
        help_text='Введите название жанра',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Страница жанра',
        help_text='Введите адрес страницы жанра, доступные символы: ^[-a-zA-Z0-9_]+$',
        unique=True,
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение',
        help_text='Введите название произведения',
    )
    year = models.IntegerField(
        max_length=4,
        verbose_name='Год создания произведения',
        help_text='Укажите год создания произведения',
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='О чем данное произведение?',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
