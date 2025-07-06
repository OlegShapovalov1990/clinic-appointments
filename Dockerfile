FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip && \
    pip install poetry


COPY pyproject.toml poetry.lock ./


RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root && \
    poetry run pip install .


COPY . .


RUN useradd -m app && \
    chown -R app:app /app

USER app


CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]