# Clinic Appointments API
Микросервис для записи пациентов на прием к врачу
- Создание и просмотр записей на прием
- Проверка уникальности времени приема у врача
- Автоматические миграции базы данных (Alembic)
- Готовый сценарий для Telegram-бота с ИИ-подбором врача

## 🛠 Технологии
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL
- **Infrastructure**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Telegram Bot**: Концепт с NLP-интеграцией

## 🚀 Быстрый старт

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/OlegShapovalov1990/email_microservice
   
2. Активируйте виртуальное окружение в корне проекта:
    ```bash
   pip install virtualenv
    python -m venv .venv 
    .\.venv\Scripts\activate # для Windows
   
3. Установите poetry в вашем виртуальном окружении
    ```bash
   python -m pip install poetry
   
4. Установите зависимости
    ```bash
   python -m poetry install
   
5. Создайте .env файл, скопировав шаблон из .env_template и пропишите переменные окружения
6. Выполните миграции - создание и применение
    ```bash
   alembic init alembic
   alembic revision --autogenerate -m "Initial tables"
   alembic upgrade head
   
Если миграции не проходят , то в alembic.ini в sqlalchemy.url заменить DATABASE_URL и явно указать путь базы данных
   
## Docker
1. Установить Docker(если у вас Windows, установите Docker Desktop и WSL): https://docs.docker.com/engine/install/ubuntu/
2. Сборка и запуск контейнеров
    ```bash
   docker-compose up -d --build

🔹 API: http://localhost:8000
- POST /appointments - создание записи
- GET /appointments/{id} - получение записи

🔹 Swagger UI: http://localhost:8000/docs

## Telegram-бот (концепт)

Сценарий работы и stub-код доступны в:
- [Документация бота,Stub-реализация](bot_scenario.md)

Для реализации потребуется:
1. Настроить вебхук на ваш FastAPI-сервер
2. Интегрировать NLP-движок (Dialogflow/Rasa)
3. Реализовать проверку свободных слотов через API


## Архитектура на диаграмме:
- [Блок схема взаимодействия](diagram)