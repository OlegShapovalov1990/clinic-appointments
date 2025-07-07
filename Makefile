.PHONY: lint test up down migrate migration initdb help

# Определение ОС
ifeq ($(OS),Windows_NT)
    DOCKER_COMPOSE := docker-compose
    DOCKER_EXEC := docker exec
    RM := del /Q /S
else
    DOCKER_COMPOSE := docker compose
    DOCKER_EXEC := docker compose exec
    RM := rm -rf
endif

# Общие команды
SLEEP := $(if $(filter Windows_NT,$(OS)),timeout,sleep)
MKDIR := $(if $(filter Windows_NT,$(OS)),mkdir,mkdir -p)

## Линтеры
lint:
    @poetry run black --check .
    @poetry run isort --check .
    @poetry run flake8 .

## Запуск тестов
test:
    @echo "Running tests..."
    @poetry run pytest -v --cov=app --cov-report=term-missing

## Запуск сервисов
up:
    @echo "Starting services..."
    @$(DOCKER_COMPOSE) up -d --build

## Остановка сервисов
down:
    @echo "Stopping services..."
    @$(DOCKER_COMPOSE) down

## Применение миграций
migrate:
    @echo "Applying migrations..."
    @$(DOCKER_EXEC) api alembic upgrade head

## Создание миграции
migration:
    @if [ -z "$(m)" ]; then \
        echo "Error: Migration message is required. Usage: make migration m=\"description\""; \
        exit 1; \
    fi
    @$(DOCKER_EXEC) api alembic revision --autogenerate -m "$(m)"

## Инициализация БД
initdb:
    @echo "Initializing database..."
    @$(DOCKER_COMPOSE) up -d db
    @$(SLEEP) 5
    @$(DOCKER_EXEC) db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB} -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
    @$(DOCKER_EXEC) api alembic upgrade head

## Справка по Makefile
help:
    @echo "Available commands:"
    @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
