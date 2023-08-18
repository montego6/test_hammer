## Тестовое задание для компании Hammer Systems
Приложение можно протестировать на [тестовом сервере](http://85.193.91.121:8000/)

## Задание
Реализовать простую реферальную систему: аутентификация по номеру телефона и по полученному на этот номер коду, профиль, в котором можно посмотреть свой инвайт-код, возможность ввести в профиле чужой инвайт-код

## Решение
В решении использованы Django, DjangoRestFramework и база данных PostgreSQL. Для аутентификации по номеру телефона была расширена модель AbstractBaseUser, для нее написан собственный менеджер, также был написан свой authentication backend для аутентификации только по номеру телефона(без пароля). Были разработаны с помощью DRF 4 endpoint-а для аутентификации, получения данных профиля и возможности заинвайтиться. Был разработан простенький web-интерфейс на JavaScript. Присутствует документация к API в формате OpenAPI, визуализированная с помощью ReDoc. Приложение можно запустить с помощью Docker-а

## API endpoints
**api/login/code/** В post запросе должен присутствовать phone_number в формате 7ХХХХХХХХХХ, в ответе будет отправлен status, detail, phone_number и code. В случае ошибки ответ будет содержать status - error и detail с описанием ошибки

**api/login/** В post запросе должен присутствовать phone_number в формате 7ХХХХХХХХХХ и code, в случае успеха пользователь будет залогинен и произойдет перенаправление на endpoint api/profile. В случае ошибки ответ будет содержать status - error и detail с описанием ошибки

**api/profile/** Get запрос, в ответе будет отправлен user, invite_code, invited_users, code_invited - соответственно телефон пользователя, его инвайт-код, список пользователей, которых он заинвайтил, и код, который он сам использовал для инвайта. В случае ошибки ответ будет содержать status - error и detail с описанием ошибки


**api/get-invited/** В post запросе должен присутствовать invite_code, в случае успеха инвайт код будет применен и вернется status - success, detail с описанием успеха. В случае ошибки ответ будет содержать status - error и detail с описанием ошибки

## Web UI
**/** Перенаправляет на страницу логина, если пользователь не залогинен, если залогинен перенаправляет на страницу профиля

**login/** Простая форма логина

**logout/** Выход

**profile/** Страница профиля

**redoc/** Страница с документацией в формате OpenApi, которая визуализирована с помощью ReDoc

## Запус приложения

### Запуск приложения с помощью Docker
В корне проекта создайте **.env** файл и пропишите в нем следующие переменные:
```
DB_NAME=app
DB_USER=postgres
DB_PASSWORD=supersecretpassword
DB_HOST=db
```
Затем мы запускаем приложение следующей Docker командой в терминале:
```
docker-compose up -d
```
Приложение запуститься и должно быть доступно по локальному адресу [127.0.0.1:8000](http://127.0.0.1:8000)

Остановить приложение/запустить заново:
```
docker-compose stop
docker-compose start
```
Остановить приложение и удалить все связанные контейнеры, включая базу данных:
```
docker-compose down -v
```
При изменениях в коде проекта, необходимо заново создать образ и запустить сервисы:
```
docker-compose build
docker-compose up -d
```

### Запуск приложения без использования Docker
Сначала в корне проекта создадим виртуальное окружение и активируем его:
```
python3 -m venv venv
source venv/bin/activate
```
Затем установим все зависимости проекта, отдав следующую команду:
```
pip install -r requirements.txt
```
После этого в корне проекта создайте **.env** файл и пропишите в нем следующие переменные:
```
DB_NAME= название вашей базы данных
DB_USER= имя пользователя
DB_PASSWORD= пароль пользователя
DB_HOST=localhost
```
***Убедитесь, что PostgreSQL запущен на локальной машине и принимает соединения на порту 5432***

Затем в корне проекта отдаем следующие команды, применяя миграции к базе данных:
```
python3 manage.py migrate
```
После этого можно запускать сервер следующей командой:
```
python3 manage.py runserver
```
Приложение запуститься и должно быть доступно по локальному адресу [127.0.0.1:8000](http://127.0.0.1:8000)