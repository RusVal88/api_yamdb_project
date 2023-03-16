from django.db import models
from django.db.models import Avg

from users.models import User


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
            'Введите адрес страницы категории,'
            'доступные символы: ^[-a-zA-Z0-9_]+$'
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
            'доступные символы: ^[-a-zA-Z0-9_]+$'
        ),
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
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.name

    def get_rating(self):
        return self.review.aggregate(Avg('estimation'))['estimation__avg']


class Review(models.Model):
    estimation_value = [(value, str(value)) for value in range(1, 11)]
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
    estimation = models.IntegerField(
        verbose_name='Оценка',
        help_text='Выберите оценку от 1 до 10',
        choices=estimation_value,
    )
    titles = models.ForeignKey(
        Titles,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review',
    )

    def __str__(self):
        return self.text[:300]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'titles', ],
                name='unique_author_titles'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comment'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Обзор',
        on_delete=models.CASCADE,
        related_name='comment'
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
