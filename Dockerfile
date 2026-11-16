FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /service

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root --no-interaction

COPY app/ ./app/

WORKDIR /service/app

EXPOSE 5000

CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "1", \
     "--timeout", "60", \
     "run:app"]