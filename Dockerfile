# syntax=docker/dockerfile:1
FROM python:3.9.18-slim-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

##############
# BUILD stage
##############
FROM base as build

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.2

# build-time OS dependencies
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get install -y \
        gcc \
        libc-dev \
        libffi-dev \
        g++

# install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# install Python dependencies in virtual environment
COPY . .
RUN poetry install

# build the app in virtual environment
RUN poetry build
RUN .venv/bin/pip install dist/*.whl
RUN mv .venv /venv

##############
# FINAL stage
##############
FROM base as final

# runtime OS dependencies
RUN apt-get install -y libstdc++ \
    && rm -rf /var/lib/apt/lists/*

# copy the built virtual environment and entry point
COPY --from=build /venv /app/.venv
COPY docker-entrypoint.sh wsgi.py ./

ENV MODEL_PATH='/app/.venv/lib/python3.9/site-packages/hmpps_person_match_score/model.json'

# create app user
RUN groupadd -g 1001 appuser && \
    useradd -u 1001 -g appuser -m -s /bin/bash appuser
USER 1001

EXPOSE 5000

CMD ["./docker-entrypoint.sh"]
