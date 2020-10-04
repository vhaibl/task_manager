##Task manager

Сервис task manager, позволяющий пользователю ставить себе задачи, отражать в системе изменение их статуса и просматривать историю задач.  
Использованы Python 3.8, Django 3.1.1, Django REST Framework 3.12.1, PostgreSQL 10  
Сервис предоставляет интерфейс в виде JSON API, авторизация происходит по токену, 
переданному в заголовке (Authorization), формат Authorization:Token 0000000000000000000000000000000000000000   
Сервис покрыт тестами(coverage report доступен в папке /htmlcov), содержит Dockerfile и docker-compose.yml 
для сборки (сборка протестирована на Ubuntu 20.04 lts и CentOS 7)  
Все пользователи могут создавать, редактировать и удалять только свои задачи.   
Суперпользователю открыт полный доступ ко всем записям.


```request
 GET yourserver/tasks/ - список задач
 POST yourserver/tasks/ - создание новой задачи
 GET yourserver/tasks/<номер задачи>/ - карточка задачи 
 PUT/DELETE yourserver/tasks/<номер задачи> - редактирование/удаление задачи 
 GET yourserver/tasks/<номер задачи>/history/ - история изменений задачи 
```

#### Использование фильтров:
Фильтр по статусу задачи:
status=[PLANNED, NEW, INPROGRESS, COMPLETED]
```http request
GET /tasks/?status=INPROGRESS
```
Вернет все задачи пользователя со статусом In progress

Фильтры по дате
planned_by__date__gte=YYYY-MM-DD  - дата начала
planned_by__date__lte=YYYY-MM-DD  - date to
Примеры:
Вернет все задачи пользователя с планируемой датой завершения начиная с 21 марта 2021:
```http request
GET /tasks/?status=&planned_by__date__gte=2020-03-21 
```

Вернет все задачи пользователя с планируемой датой зазаканчивая 31 января 2021

```http request
GET /tasks/?status=&planned_by__date__lte=2021-01-31
```
Вернет все задачи пользователя с диапазоном завершения от 21 марта 2020 до 31 января 2021
```http request
GET /tasks/?status=&planned_by__date__gte=2020-03-21&planned_by__date__lte=2021-01-31

```

Фильтры можно комбинировать:
Вернет все задачи пользователя со статусом In progress в диапазоне завершения от 9 сентября 2020 до 21 января 2021

```http request
GET /tasks/?status=INPROGRESS&planned_by__date__gte=2020-09-30&planned_by__date__lte=2021-01-21
```


#### Действия с пользователями

Регистрация пользователя:
POST yourserver/auth/registration/
```json
{ "username": "имя",  
"password1": "пароль",
"password2": "подтверждение пароля"} 
```
Получение токена:
POST yourserver/auth/login/
```json
{ "username": "имя",  
"password": "пароль"}
```
Информация о пользователе:
GET yourserver/auth/user/
```json
{"Authorization": "Token 0000000000000000000000000000000000000000/"}
```
Смена пароля:
POST yourserver/auth/password/change/
```json
{ "old_password": "старый пароль",  
"new_password1": "пароль",
"new_password2": "подтверждение пароля"} 
```

#### Установка
В PostgreSQL создать базу tododb принадлежащую django_admin:
```postgresql

create user django_admin with password 'django_pass';
alter role django_admin set client_encoding to 'utf8';
alter role django_admin set default_transaction_isolation to 'read committed';
alter role django_admin set timezone to 'UTC';

create database tododb owner django_admin; 
```
запустить миграцию:
```commandline
python3 manage.py migrate
python3 manage.py migrate --run-syncdb
```
загрузить дамп базы:
```commandline
python3 manage.py loaddata data.json

```
запустить сервис:
```commandline
python3 manage.py runserver

```

для тестов можно использовать двух пользователей:  
admin:admin - суперпользовать  
user:user1234 - staff  