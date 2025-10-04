# Task Manager (Django, Hexlet)

[![hexlet-check](https://github.com/D4rkli/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/D4rkli/python-project-52/actions/workflows/hexlet-check.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=D4rkli_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=D4rkli_python-project-52)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=D4rkli_python-project-52&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=D4rkli_python-project-52)

Минимальный таск‑менеджер: пользователи, статусы, метки и задачи с фильтрацией. UI на Bootstrap, сервер на Django.

**Демо:** https://python-project-52-l36d.onrender.com

---

## Возможности

- Регистрация, вход/выход, редактирование и удаление своего профиля.  
- CRUD для **статусов** и **меток** (удаление запрещено, если есть связанные задачи).  
- CRUD для **задач** + страница просмотра.  
- Связи:
  - Задача → Статус: `ForeignKey(PROTECT)`
  - Задача → Автор: `ForeignKey(PROTECT)`
  - Задача → Исполнитель: `ForeignKey(PROTECT, null=True, blank=True)`
  - Задача ↔ Метки: `ManyToMany`
- Фильтрация задач по статусу, исполнителю, меткам и «только мои».
- Flash‑сообщения (Bootstrap alerts).
- Статика через WhiteNoise.

---

## Технологии

- Python 3.10+
- Django 5, django-filter, django-bootstrap5
- gunicorn, whitenoise
- psycopg2-binary (PostgreSQL в продакшене)
- uv (менеджер пакетов)
- (опц.) Rollbar для отслеживания ошибок

---

## Структура проекта

```
hexlet-code/
  manage.py
  task_manager/
    settings.py
    urls.py
    ...
    users/
    statuses/
    labels/
    tasks/
  staticfiles/           # для collectstatic (в проде)
```

Модуль доступен как пакет:

```python
from task_manager import settings
```

---

## Быстрый старт (локально)

### 1) Клонирование и окружение

```bash
git clone <repo-url>
cd hexlet-code
cp .env.example .env  # если есть
```

Пример `.env` (локально, sqlite):

```
DEBUG=1
SECRET_KEY=please_change_me
DJANGO_SETTINGS_MODULE=task_manager.settings
# DATABASE_URL=postgres://user:pass@localhost:5432/dbname  # (опционально)
# ROLLBAR_ACCESS_TOKEN=...
# ROLLBAR_ENV=development
```

### 2) Установка зависимостей

Через **uv** (рекомендовано):

```bash
# если uv не установлен
curl -LsSf https://astral.sh/uv/install.sh | sh
# зависимости
uv pip install -r requirements.txt
```

Через **pip**:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3) Миграции, старт и вход

```bash
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
# по желанию:
python manage.py createsuperuser
```


---

## Тесты, линтер, форматирование

```bash
# pytest
pytest -vv

# Ruff (линт)
ruff check .

# Ruff (автопочинка)
ruff check --fix .

# Форматирование Ruff
ruff format .
```
---

## Деплой на Render (PaaS)

1. Создай аккаунт на https://render.com и привяжи Git‑репозиторий.  
2. Создай **Web Service**, укажи:
   - **Build Command:** `make build`
   - **Start Command:** `make render-start`
3. Переменные окружения:
   - `DJANGO_SETTINGS_MODULE=task_manager.settings`
   - `SECRET_KEY=<случайная_строка>`
   - `DEBUG=0`
   - `DATABASE_URL=<PostgreSQL URL из Render>`
   - (опц.) `ROLLBAR_ACCESS_TOKEN`, `ROLLBAR_ENV=production`
4. Подключи **Render PostgreSQL** и скопируй DSN в `DATABASE_URL`.  
5. Убедись, что в `ALLOWED_HOSTS` прописаны `webserver` (для тестов/докера) и домен Render.

### `build.sh` (пример)

```bash
#!/usr/bin/env bash
set -e

# установить uv на билд‑машину
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

# зависимости + сборка
make install
make collectstatic
make migrate
```

> На Render порт нужно брать из переменной окружения `$PORT` (см. `render-start` в Makefile).

### Подсказки по продакшену

- Статику отдаёт **WhiteNoise**; обязательно `collectstatic` на билде.  
- Секреты держи в переменных окружения.  
- Если ловишь ошибку версии Python — удали `.python-version` из репозитория.  
- База локально — sqlite, в проде — PostgreSQL через `dj-database-url`.

---

## Маршруты

| Раздел       | Роуты |
|--------------|-------|
| Главная      | `GET /` |
| Пользователи | `GET /users/`, `GET/POST /users/create/`, `GET/POST /users/<id>/update/`, `GET/POST /users/<id>/delete/` |
| Сессия       | `GET/POST /login/`, `POST /logout/` |
| Статусы      | `GET /statuses/`, `GET/POST /statuses/create/`, `GET/POST /statuses/<id>/update/`, `GET/POST /statuses/<id>/delete/` |
| Метки        | `GET /labels/`, `GET/POST /labels/create/`, `GET/POST /labels/<id>/update/`, `GET/POST /labels/<id>/delete/` |
| Задачи       | `GET /tasks/`, `GET/POST /tasks/create/`, `GET /tasks/<id>/`, `GET/POST /tasks/<id>/update/`, `GET/POST /tasks/<id>/delete/` |

---

## Сообщения (для автотестов)

- **Вход:** «Вы залогинены».  
- **Выход:** «Вы разлогинены».  
- **Пользователь:** создан/изменён/удалён — «Пользователь успешно …»; запрет на чужие изменения — «У вас нет прав для изменения…» / «Вы не имеете прав для удаления другого пользователя».  
- **Статусы/Метки:** «… успешно …»; защищённое удаление — «Невозможно удалить …, потому что … используется».  
- **Задачи:** «Задача успешно …»; удалять может только автор — «Задачу может удалить только ее автор».

---

## UI

- Django Templates + Bootstrap 5 (CDN).
- Сообщения (`messages`) выводятся в `base.html` единым блоком.
- Язык интерфейса — русский.

---

## Логи и ошибки

- (Опц.) Rollbar: переменные окружения `ROLLBAR_*`.
- Логи сервера — в панели Render.

---

## Лицензия

MIT
