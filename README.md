# Сервис Благотворительного фонда поддержки котиков QRKot

### Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

<img alt=”Python” src="https://img.shields.io/badge/-Python-brightgreen?style=for-the-badge&logo=micropython"/>

Приложение представляет собой API сервис написанный на python 3.9.2 c использованием фреймворка FastAPI.

Основные настройки программы офрмлены в файле `app/core/config.py`, так же приложение по умолчание создает суперпользователя (админа) при установке, с логином и паролем указанным в настройках. Для отключения этой функции закоментируйте или удалите следущие строки в файле `main.py`

```
@app.on_event('startup')
async def startup():
    await create_first_superuser()
```

#### Требуемые приложения для установки (requirements)

aiosqlite==0.17.0
alembic==1.7.7
anyio==3.6.1
asgiref==3.5.2
attrs==21.4.0
bcrypt==3.2.2
certifi==2022.5.18.1
cffi==1.15.0
charset-normalizer==2.0.12
click==8.1.3
cryptography==37.0.2
dnspython==2.2.1
email-validator==1.2.1
faker==12.0.1
fastapi-users-db-sqlalchemy==4.0.3
fastapi-users[sqlalchemy]==10.0.4
fastapi==0.78.0
flake8==4.0.1
freezegun==1.2.1
greenlet==1.1.2
h11==0.13.0
httptools==0.4.0
idna==3.3
iniconfig==1.1.1
makefun==1.13.1
mako==1.2.0
markupsafe==2.1.1
mccabe==0.6.1
mixer==7.2.2
packaging==21.3; python_version >= '3.6'
passlib[bcrypt]==1.7.4
pluggy==1.0.0
py==1.11.0
pycodestyle==2.8.0
pycparser==2.21
pydantic==1.9.1
pyflakes==2.4.0
pyjwt[crypto]==2.3.0
pyparsing==3.0.9
pytest-asyncio==0.18.3
pytest-freezegun==0.4.2
pytest-pythonpath==0.7.4
pytest==6.2.5
python-dateutil==2.8.2
python-dotenv==0.20.0
python-multipart==0.0.5
pyyaml==6.0
requests==2.27.1
six==1.16.0
sniffio==1.2.0
sqlalchemy==1.4.36
starlette==0.19.1
toml==0.10.2
typing-extensions==4.2.0
urllib3==1.26.9
uvicorn[standard]==0.17.6
watchgod==0.8.2
websockets==10.3

### УСТАНОВКА И ЗАПУСК ПРИЛОЖЕНИЯ

Скопируйте себе проект

`git clone git@github.com:offon/cat_charity_fund.git`

Создайте и активируйте виртуальное окружение

```
python3 -m venv venv
. venv/bin/activate
```

Установите необходимые пакеты для работы приложения

`pip install -r requirements.txt`

Выполните команды для создания базы данных и проведение необходимых миграций
```
alembic init --template async alembic
alembic revision --autogenerate -m "First migration"
alembic upgrade head
```

Для запуска приложение можете воспользоваться командой

`uvicorn app.main:app --reload`

Документация по запросам можно найти по ссылкам `/docs`, `/redoc`

### ПРИМЕРЫ ЗАПРОСОВ И ОТВЕТОВ ПРИЛОЖЕНИЯ


### /charity_project/

#### GET
##### Summary:

Get All Charity Projects

##### Description:

Получает список всех проектов.

##### Responses

```
[
  {
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2023-03-06T12:59:47.707Z",
    "close_date": "2023-03-06T12:59:47.707Z"
  }
]
```

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |


#### POST
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```
##### Summary:

Create Charity Project

##### Description:

Только для суперюзеров.

Создает благотворительный проект.

##### Responses
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-03-06T13:00:35.260Z",
  "close_date": "2023-03-06T13:00:35.260Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /charity_project/{project_id}

#### DELETE
##### Summary:

Delete Charity Project

##### Description:

Только для суперюзеров.

Удаляет проект.
Нельзя удалить проект, в который уже были инвестированы средства,
его можно только закрыть.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| project_id | path |  | Yes | integer |

##### Responses
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-03-06T13:01:59.917Z",
  "close_date": "2023-03-06T13:01:59.917Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

#### PATCH
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0
}
```
##### Summary:

Update Charity Project

##### Description:

Только для суперюзеров.

Закрытый проект нельзя редактировать,
также нельзя установить требуемую сумму меньше уже вложенной.

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| project_id | path |  | Yes | integer |

##### Responses
```
{
  "name": "string",
  "description": "string",
  "full_amount": 0,
  "id": 0,
  "invested_amount": 0,
  "fully_invested": true,
  "create_date": "2023-03-06T13:02:21.948Z",
  "close_date": "2023-03-06T13:02:21.948Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /donation/

#### GET
##### Summary:

Get All Donations

##### Description:

Только для суперюзеров.

Получает список всех пожертвований.

##### Responses
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2023-03-06T13:03:35.381Z",
    "user_id": "string",
    "invested_amount": 0,
    "fully_invested": true,
    "close_date": "2023-03-06T13:03:35.381Z"
  }
]
```

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

#### POST
```
{
  "full_amount": 0,
  "comment": "string"
}
```
##### Summary:

Create Donation

##### Description:

Сделать пожертвование.

##### Responses
```
{
  "full_amount": 0,
  "comment": "string",
  "id": 0,
  "create_date": "2023-03-06T13:03:51.610Z"
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /donation/my

#### GET
##### Summary:

Get User Donations

##### Description:

Получить список моих пожертвований.

##### Responses
```
[
  {
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2023-03-06T13:05:23.892Z"
  }
]
```

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /auth/jwt/login

#### POST

##### Summary:

Auth:Jwt.Login

##### Responses

```
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
  "token_type": "bearer"
}
```

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |

### /auth/jwt/logout

#### POST
##### Summary:

Auth:Jwt.Logout

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 401 | Missing token or inactive user. |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /auth/register

#### POST
```
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
##### Summary:

Register:Register

##### Responses
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

| Code | Description |
| ---- | ----------- |
| 201 | Successful Response |
| 400 | Bad Request |
| 422 | Validation Error |

### /users/me

#### GET
##### Summary:

Users:Current User

##### Responses
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 401 | Missing token or inactive user. |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

#### PATCH
```
{
  "password": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": true,
  "is_verified": true
}
```
##### Summary:

Users:Patch Current User

##### Responses
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 401 | Missing token or inactive user. |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

### /users/{id}

#### GET
##### Summary:

Users:User

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string (uuid4) |

##### Responses
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 401 | Missing token or inactive user. |
| 403 | Not a superuser. |
| 404 | The user does not exist. |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |

#### PATCH
```
{
  "password": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": true,
  "is_verified": true
}
```
##### Summary:

Users:Patch User

##### Parameters

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| id | path |  | Yes | string (uuid4) |

##### Responses
```
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```
| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |
| 400 | Bad Request |
| 401 | Missing token or inactive user. |
| 403 | Not a superuser. |
| 404 | The user does not exist. |
| 422 | Validation Error |

##### Security

| Security Schema | Scopes |
| --- | --- |
| OAuth2PasswordBearer | |


### /google/

#### GET
##### Summary:

Create report for closed projects, ordering by speed of closed

##### Description:

Формирует список закрытых проектов сортированных по скорости закрытия

##### Responses

| Code | Description |
| ---- | ----------- |
| 200 | Successful Response |