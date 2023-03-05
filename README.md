# Проект Foodgram
[![foodgram workflow](https://github.com/gutolin/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/gutolin/foodgram-project-react/actions/workflows/main.yml)
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

Проект запущен по [адресу](http://158.160.19.61)

Foodgram реализован для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

## Подготовка и запуск проекта

* Установка docker на сервер:
```
sudo apt install docker.io 
```
* Установка docker-compose на сервер:
```
sudo apt install docker-compose
```
* Скопируйте файлы docker-compose.yml из корня и nginx.conf из директории infra на сервер:

* Cоздайте .env файл и впишите:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<название БД>
    DB_USER=<пользователь бд>
    DB_PASSWORD=<пароль>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<секретный ключ проекта django>
    ```
* Запуск контейнера docker'a на сервере:
```
sudo docker-compose up -d --build
```
* Подготовка django сервера к работе:
    - Сбор файлов статики:
    ```
    sudo docker-compose exec web python manage.py collectstatic --noinput
    ```
    - Применение миграций:
    ```
    sudo docker-compose exec web python manage.py migrate --noinput
    ```
    - Загрузка ингридиентов в БД:
    ```
    sudo docker-compose exec web python manage.py import_data
    ```
    - Создание суперпользователя Django:
    ```
    sudo docker-compose exec web python manage.py createsuperuser
    ```