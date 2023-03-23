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

        self.load_data_from_csv(
            'users.csv', User, id='id', username='username', email='email',
            role='role', bio='bio'
        )
        self.load_data_from_csv(
            'category.csv', Category, id='id', name='name', slug='slug'
        )
        self.load_data_from_csv(
            'genre.csv', Genre, id='id', name='name', slug='slug'
        )
        self.load_data_from_csv(
            'titles.csv', Title, id='id', name='name', year='year',
            category_id='category'
        )
        self.load_data_from_csv(
            'genre_title.csv', GenreTitle, id='id', title_id='title_id',
            genre_id='genre_id'
        )
        self.load_data_from_csv(
            'review.csv', Review, id='id', title_id='title_id', text='text',
            author_id='author', score='score', pub_date='pub_date'
        )
        self.load_data_from_csv(
            'comments.csv', Comment, id='id', review_id='review_id',
            text='text', author_id='author', pub_date='pub_date'
        )

        print('Данные загружены')

    def load_data_from_csv(self, filename, model_class, **field_names):
        try:
            with open(
                f'./static/data/{filename}', encoding='utf-8'
            ) as csv_file:
                for row in csv.DictReader(csv_file):
                    kwargs = {}
                    for field_name, csv_column_name in field_names.items():
                        kwargs[field_name] = row[csv_column_name]
                    model_instance = model_class(**kwargs)
                    model_instance.save()
        except ValueError:
            print('Значение неопределенно')
        except Exception:
            print('Возникла непредвиденная ситуация')
