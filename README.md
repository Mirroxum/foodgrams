![yamdb workflow](https://github.com/Mirroxum/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Краткое описание проекта YaMDb

Cайт Foodgram, «Продуктовый помощник». Онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Проект находится по адресу:
```
http://51.250.74.213/
```
Админ-панель:
```
e-mail: a@a.ru
password: Admin
```

### Стек технологий

![gunicorn](https://img.shields.io/badge/gunicorn-blue) ![Nginx](https://img.shields.io/badge/Nginx-green) ![Docker](https://img.shields.io/badge/Docker-blue) ![Docker-compose](https://img.shields.io/badge/Docker--compose-red) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue) ![Django](https://img.shields.io/badge/Django-green) ![React](https://img.shields.io/badge/React-blue)


### Шаблон наполнения env-файла

```
SECRET_KEY=Секретный ключ
DB_ENGINE=Подсистема хранения (для postgresql - django.db.backends.postgresql)
DB_NAME=Имя базы данных
POSTGRES_USER=Логин для подключения к базе данных
POSTGRES_PASSWORD=Пароль для подключения к БД
DB_HOST=Название сервиса (контейнера)
DB_PORT=Порт для подключения к БД
```


### Запуск контейнеров и приложений в нем

Перейти в репозиторий для запуска докера

```
cd infra/
```

Запуск docker-compose

```
docker-compose up -d --build
```

Выполните по очереди команды:
```
docker-compose exec backend python manage.py migrate
```
```
docker-compose exec backend python manage.py createsuperuser
```
```
docker-compose exec backend python manage.py collectstatic --no-input
```
Войдите в админку и создайте записи объектов.

Или выполните команду
```
docker-compose exec backend python manage.py runscript load_data
```
что бы заполнить базу данными ингредиентов
