


#### Действия с пользователями

Авторизация по токену, формат:
```
Authorization:Token 0000000000000000000000000000000000000000
```               

Регистрация пользователя:
 
POST yourserver/auth/registration/
```json
{ "username": "имя",  
"password1": "пароль"  
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
"new_password1": "пароль"  
"new_password2": "подтверждение пароля"} 
```

### Тесты:
для тестов создается база SQLite (удаляется по заверщению автоматически)
Отчёт Coverage в /htmlconv/ (покрытие приложения 'todo' - 100%)



В постгрес, создать базу tododb принадлежащую django_admin:
```postgresql

create user django_admin with password 'django_pass';
alter role django_admin set client_encoding to 'utf8';
alter role django_admin set default_transaction_isolation to 'read committed';
alter role django_admin set timezone to 'UTC';

create database tododb owner django_admin; 
```
при необходимости сконвертировать дамп базы в utf8:
```commandline
iconv -f cp1251 -t utf-8 data.json  -o dump.json
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
