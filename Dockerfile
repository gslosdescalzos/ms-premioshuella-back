FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

RUN pip install --no-cache-dir poetry==1.8.5

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 appgroup \
    && useradd --uid 1000 --gid appgroup --shell /usr/sbin/nologin --create-home appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appgroup . .

COPY --chown=appuser:appgroup entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
