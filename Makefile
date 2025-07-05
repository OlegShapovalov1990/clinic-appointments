.PHONY: lint test up down migrate initdb

# Определяем ОС
ifeq ($(OS),Windows_NT)
    DOCKER_COMPOSE = docker-compose
    DOCKER_EXEC = docker exec
    MKDIR = mkdir
    RM = del /Q
    SLEEP = timeout
else
    DOCKER_COMPOSE = docker compose
    DOCKER_EXEC = docker compose exec
    MKDIR = mkdir -p
    RM = rm -f
    SLEEP = sleep
endif

lint:
	poetry run black --check .
	poetry run isort --check .
	poetry run flake8 .

test:
	poetry run pytest -v

up:
	$(DOCKER_COMPOSE) up -d --build

down:
	$(DOCKER_COMPOSE) down

migrate:
	$(DOCKER_EXEC) api alembic upgrade head

migration:
	$(DOCKER_EXEC) api alembic revision --autogenerate -m "$(m)"

initdb:
	$(DOCKER_COMPOSE) up -d db
	$(SLEEP) 5
	$(DOCKER_EXEC) db psql -U $${POSTGRES_USER} -d $${POSTGRES_DB} -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
	$(DOCKER_EXEC) api alembic upgrade head