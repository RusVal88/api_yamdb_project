import csv

from django.core.management import BaseCommand

from reviews.models import Category, Genre, Title, Review, Comment, GenreTitle
from users.models import User

ERROR_MESSAGE = """
Ошибка! В БД уже есть данные. Для обновления требуется удалить
db.sqlite3 и заново провести миграции для создания пустой БД
"""


class Command(BaseCommand):

    def handle(self, *args, **options,):
        DB_TABLES = [User, Title, Category, Comment, Genre, GenreTitle, Review]
        for table in DB_TABLES:
            if table.objects.exists():
                print(ERROR_MESSAGE)
                return

        try:
            for row in csv.DictReader(
                open('./static/data/users.csv', encoding='utf-8')
            ):
                new_table  = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/category.csv', encoding='utf-8')
            ):
                new_table  = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/genre.csv', encoding='utf-8')
            ):
                new_table  = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/titles.csv', encoding='utf-8')
            ):
                new_table  = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=Category.objects.get(pk=row['category']),
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/genre_title.csv', encoding='utf-8')
            ):
                new_table  = GenreTitle(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    genre=Genre.objects.get(pk=row['genre_id']),
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/review.csv', encoding='utf-8')
            ):
                new_table  = Review(
                    id=row['id'],
                    title=Title.objects.get(pk=row['title_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                new_table .save()
            for row in csv.DictReader(
                open('./static/data/comments.csv', encoding='utf-8')
            ):
                new_table  = Comment(
                    id=row['id'],
                    review=Review.objects.get(pk=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(pk=row['author']),
                    pub_date=row['pub_date'],
                )
                new_table .save()
        except ValueError:
            print('Значение неопределенно')
        except Exception:
            print('Возникла непредвиденная ситуация')
        else:
            print('Данные загружены')
