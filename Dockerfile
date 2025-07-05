FROM python:3.12-slim

WORKDIR /app

RUN useradd -m app && \
    chown -R app:app /app

USER app

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --chown=app:app pyproject.toml poetry.lock ./

RUN python -m pip install --upgrade pip && \
    python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main

COPY --chown=app:app . .

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["sh", "-c", "alembic upgrade head && poetry run python -m app.main"]