# Generated by Django 3.2 on 2023-03-17 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0003_alter_titles_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию', null=True, on_delete=django.db.models.deletion.SET_NULL, to='review.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанр', to='review.Genre', verbose_name='Жанр'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.IntegerField(help_text='Укажите год создания произведения', verbose_name='Год создания'),
        ),
    ]
