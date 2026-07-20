# GameCore AI

Персональный интеллектуальный игровой ассистент в Telegram.
Сейчас — закрытое тестирование (работает только для владельца), архитектура рассчитана на масштабирование до десятков тысяч пользователей без переписывания.

## Стек

Python 3.13 · aiogram 3 · SQLAlchemy 2 (async) · Alembic · SQLite · OpenRouter · Pydantic Settings · Loguru · uv

## Быстрый старт

```bash
# 1. Установи uv: https://docs.astral.sh/uv/
# 2. Установи зависимости (Python 3.13 подтянется автоматически)
uv sync

# 3. Настрой окружение
cp .env.example .env   # впиши BOT_TOKEN и BOT_OWNER_ID

# 4. Применяй миграции
uv run alembic upgrade head

# 5. Запускай
uv run python -m app.main
```

## Структура

```
app/
  main.py            — точка входа (composition root)
  config/            — настройки из .env (Pydantic Settings, по группам)
  core/              — ядро: DI-контейнер, система модулей, логирование, исключения
  database/          — движок SQLAlchemy, декларативная база
  models/            — ORM-модели
  repositories/      — слой доступа к данным (единственное место с SQL)
  middleware/        — доступ (owner-only), сессия БД, DI, логирование
  handlers/          — базовые Telegram-хендлеры (/start, меню, ошибки)
  keyboards/         — клавиатуры (типизированные callback'и)
  routers/           — сборка корневого роутера
  modules/           — подключаемые возможности (ai, roblox, fnf, profile, community, premium)
  schemas/           — Pydantic DTO между слоями
  services/          — общие кросс-модульные сервисы
  utils/             — чистые утилиты
migrations/          — Alembic (async)
tests/               — pytest
```

Каждая крупная возможность — модуль в `app/modules/` со своим роутером, сервисами и жизненным циклом. Добавление возможности = новый пакет + одна строка в `app/modules/registry.py`.

## Разработка

```bash
uv run pytest        # тесты
uv run ruff check .  # линтер
uv run alembic revision --autogenerate -m "описание"  # новая миграция
```
