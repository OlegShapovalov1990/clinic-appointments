.PHONY: lint test up down migrate migration initdb help

# Определение ОС
ifeq ($(OS),Windows_NT)
DOCKER_COMPOSE := docker-compose
DOCKER_EXEC    := docker exec
RM             := del /Q /S
else
DOCKER_COMPOSE := docker compose
DOCKER_EXEC    := docker compose exec
RM             := rm -rf
endif

SLEEP := $(if $(filter Windows_NT,$(OS)),timeout,sleep)
MKDIR := $(if $(filter Windows_NT,$(OS)),mkdir,mkdir -p)

## Линтеры и авто-формат
lint:
	@echo "Running linters..."
	@poetry run black --check .
	@poetry run isort --check .
	@poetry run flake8 app

## Запуск тестов
test:
	@echo "Running tests..."
	@poetry run pytest -v --cov=app --cov-report=term-missing

up:
	@echo "Starting services..."
	@$(DOCKER_COMPOSE) up -d --build

down:
	@echo "Stopping services..."
	@$(DOCKER_COMPOSE) down

migrate:
	@echo "Applying migrations..."
	@$(DOCKER_EXEC) api alembic upgrade head

migration:
	@if [ -z "$(m)" ]; then \
      echo "Error: migration message required (make migration m=\"desc\")"; \
      exit 1; \
    fi
	@$(DOCKER_EXEC) api alembic revision --autogenerate -m "$(m)"

initdb:
	@echo "Initializing database..."
	@$(DOCKER_COMPOSE) up -d db
	@$(SLEEP) 5
	@$(DOCKER_EXEC) db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB} \
        -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
	@$(DOCKER_EXEC) api alembic upgrade head

help:
    @echo "Available commands:"
    @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / { \
      printf "  %-15s %s\n", $$1, $$2 \
    }' $(MAKEFILE_LIST)



