**Описание проекта:**

**YaMDb** - это api для проекта, посвящённому отзывам о книгах, фильмах, музыке и других произведениях. Произведения делятся на категории и жанры. Пользователи могут оставлять свои отзывы и ставить оценки произведениям и комментировать отзывы других пользователей.

**Возможности API:**

- Регистрация пользователей и токен авторизации (Simple JWT).
- Получение, создание, обновление, удаление учетных записей.
- Получение, создание, обновление, удаление произведений.
- Получение, создание, удаление категорий произведений и их жанров.
- Получение, создание, обновление, удаление отзывов и комментариев.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:Dewar6/api_yamdb.git
```

```
cd api_yambd
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
