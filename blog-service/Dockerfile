FROM python:3.11-slim-bookworm as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=0

RUN groupadd -g 1000 blog
RUN useradd -m -g blog -s /bin/bash -u 1000 blog

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --no-ansi

RUN chown -R blog:blog /app
USER blog
COPY src ./src
COPY start.sh .
ENV PYTHONPATH="${PYTHONPATH}:/app/src/"

ENTRYPOINT ["sh", "./start.sh"]
