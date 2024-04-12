Дипломный проект: Сервис авторизации по номеру телефона

 ## Описание ##
Сервис авторизации по номеру телефона
Интерфейс системы содержит:
 - Регистрацию по номеру телефона
 - Авторизацию по номеру телефона
 - Просмотр данных профиля
 - Редактирование профиля
При введении номера телефона, присылается код подтверждения.
Если номер вводится впервые, то он добавляется в БД. 
Реализована проверка корректности номера телефона, проверка существования кода приглашения,
проверка на повторный ввод другого кода приглашения, очистка кода подтверждения по 
истечении 2 минут по соображениям безопасности.
В проекте используется имитация отправки кода подтверждения

Для запуска проекта выполнить команду:
 - docker-compose up --build

Стек технологий:
 - Python 
 - Django 
 - DRF 
 - PostgreSQL
 - Celery
 - Docker

## Api ##

Ввод номера

POST: http://127.0.0.1:8000/users/initialization/

Пример запроса:
{
    "phone": "89234440000"
}

Результат:
[
    "Код отправлен"
]

Авторизация

POST: http://127.0.0.1:8000/users/authentication/

Пример запроса:
{
    "phone": "89234440000",
    "code":"4547"
}

Результат:
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6
MTcxMjk3MTEyNSwiaWF0IjoxNzEyODg0NzI1LCJqdGkiOiIwZDE1NDFhNjg5ZWQ0ZTU0YjdjODgwYzQwNTZkZTI1MyIsI
nVzZXJfaWQiOjJ9.LVvb7s_vSsmXb4IbGOZNIDSjxgZFahNXGPykDvv-akg",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxN
zEyOTAyNzI1LCJpYXQiOjE3MTI4ODQ3MjUsImp0aSI6IjZjNWIzZjhjMDE1ZTRiMmE4ZDhiMDdlMmQzNTBhNGY4IiwidX
Nlcl9pZCI6Mn0.L_nAyCjdjoYEXZyzUugYzHARrmL7BUUjNF267RjescI"
}

Просмотр профиля

GET: http://127.0.0.1:8000/users/profile/89234440000/

Результат:
{
    "phone": "89234440000",
    "email": null,
    "invite_code": "jSaHsu",
    "activated_invite_code": null,
    "invited_users": []
}

Редактирование профиля

PATCH: http://127.0.0.1:8000/users/profile/89234440000/

Пример запроса:
{
    "activated_invite_code": "G5k9zY"
}

Результат:
{
    "phone": "89234440000",
    "invite_code": "pMXOm1",
    "activated_invite_code": "G5k9zY",
    "invited_users": []
}



