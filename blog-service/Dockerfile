FROM python:3.11-slim-bookworm as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

RUN groupadd -g 1000 blog
RUN useradd -m -g blog -s /bin/bash -u 1000 blog

# Create app placeholder dir
RUN mkdir /app && chown -R blog:blog /app

WORKDIR /app

FROM base as builder
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
ENV PATH="/home/blog/.local/bin:${PATH}"

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root --no-interaction --no-ansi

FROM base as runtime
COPY --from=builder /app/.venv ./.venv

RUN chown -R blog:blog /app
USER blog

ENV PATH="/app/.venv/bin:${PATH}"
ENV VIRTUAL_ENV="/app/.venv"

COPY src ./src
COPY start.sh .
ENV PYTHONPATH="${PYTHONPATH}:/app/src/"

ENTRYPOINT ["sh", "./start.sh"]
