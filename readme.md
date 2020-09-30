


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
