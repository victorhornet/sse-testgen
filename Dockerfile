# syntax=docker/dockerfile:1

# Set the Python version to use
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set environment variables for Pynguin CLI
ENV PYNGUIN_DANGER_AWARE=1
ENV PYTHONHASHSEED=0

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install "pynguin==0.40.0"

COPY pynguin-docker.sh ./

RUN chmod +x pynguin-docker.sh

USER appuser

ENTRYPOINT [ "/app/pynguin-docker.sh" ]
