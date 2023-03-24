from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers

from api.validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Категория',
        help_text='Введите название категории',
    )
    slug = models.SlugField(
        max_length=50,
        verbose_name='Страница категории',
        help_text=(
            'Введите адрес категории'

        ),
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
        help_text=(
            'Введите адрес страницы жанра,'
        ),
        unique=True,
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        help_text='Выберите категорию',
        null=True,
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        help_text='Выберите жанр',
        through='GenreTitle'
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text='О чем данное произведение?',
        blank=True,
        null=True,
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Рейтинг',
    )
    year = models.IntegerField(
        verbose_name='Год создания',
        help_text='Укажите год создания произведения',
        validators=[validate_year],
        db_index=True,
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Произведение',
        help_text='Введите название произведения',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    score_value = [(value, str(value)) for value in range(1, 11)]
    heading = models.CharField(
        verbose_name='Заголовок',
        help_text='Введите заголовок обзора',
        max_length=256,
    )
    text = models.TextField(
        verbose_name='Текст',
        help_text='Напишите обзор',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор обзора',
        on_delete=models.CASCADE,
        related_name='review',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Выберите оценку от 1 до 10',
        choices=score_value,
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review',
    )

    def clean(self):
        if self.score not in list(zip(*Review.score_value))[0]:
            raise serializers.ValidationError(
                'Переданное значение "score" недопустимо.'
                'Укажите число от 1 до 10.'
            )

    def __str__(self):
        return self.text[:300]

    class Meta:
        unique_together = ('author', 'title')


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Обзор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Напишите ваш комментарий'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    def __str__(self):
        return self.text[:50]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    def __str__(self):
        return f'{self.title}, жанр: {self.genre}'
