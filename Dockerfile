FROM python:3.13-slim AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.0.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
        netcat-openbsd

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root

FROM python-base AS development
ENV DJANGO_ENV=development
WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq-dev netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python-base AS production
ENV DJANGO_ENV=production
WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]
