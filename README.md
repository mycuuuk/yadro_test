#  Сервис сокращения ссылок

REST API для создания коротких ссылок с поддержкой статистики, авторизации и срока действия.

##  Установка и запуск

```bash
git clone https://github.com/mycuuuk/yadro_test.git

cd yadro_test
pip install -r requirements.txt
sudo mysql
### Внутри mysql
CREATE DATABASE shortener_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'yadro'@'localhost' IDENTIFIED BY 'test';
GRANT ALL PRIVILEGES ON shortener_db.* TO 'yadro'@'localhost';
FLUSH PRIVILEGES;
exit
###

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
python manage.py runserver
```

##  Функциональность

- Публичный редирект по короткой ссылке: `/{short_code}/`
- Приватные эндпоинты для управления ссылками:
  - Создание ссылки с ограничением по времени
  - Получение списка ссылок
  - Деактивация
  - Статистика переходов (всего, за час, за сутки)
- Поддержка Basic Auth
- Swagger-документация: `/docs/`
- OpenAPI ReDoc: `/redoc/`

##  Авторизация

Для приватных эндпоинтов используется Basic Auth.  
В Swagger нажмите **Authorize**, введите логин/пароль суперпользователя.

##  Эндпоинты

###  Публичные

| Метод | URL              | Описание                        |
|-------|------------------|---------------------------------|
| GET   | `/{short_code}/` | Редирект по короткой ссылке     |

###  Приватные (требуется Basic Auth)

| Метод | URL                                  | Описание                        |
|-------|--------------------------------------|---------------------------------|
| POST  | `/api/links/create/`                 | Создать короткую ссылку         |
| GET   | `/api/links/`                        | Получить список своих ссылок    |
| POST  | `/api/links/{id}/deactivate/`        | Деактивировать ссылку           |
| GET   | `/api/statistics/?sort_by=...`       | Получить статистику ссылок      |

Параметры для `sort_by`:
- `total` — по общему числу переходов (по умолчанию)
- `hour` — за последний час
- `day` — за последние сутки

## Поля статистики

Каждая ссылка возвращает следующие дополнительные поля:

- `click_count` — общее количество переходов
- `clicks_last_hour` — переходы за последний час
- `clicks_last_day` — переходы за последние 24 часа

## Swagger и ReDoc

- Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
- ReDoc UI: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)



