# syntax=docker/dockerfile:1
FROM python:3.9.12-slim-buster as base

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
    POETRY_VERSION=1.4.2

# build-time OS dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    libffi-dev \
    g++

# install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# create virtual environment
RUN python -m venv /venv

# install Python dependencies in virtual environment
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt
# Remove unwanted Windows dependencies
RUN cat ./requirements.txt | sed -e :a -e '/\\$/N; s/\\\n//; ta' | sed 's/^pywin32==.*//' > requirements.txt
RUN /venv/bin/pip install -r requirements.txt

# build the app in virtual environment
COPY . .
RUN poetry build
RUN /venv/bin/pip install dist/*.whl

##############
# FINAL stage
##############
FROM base as final

ENV MODEL_PATH='/venv/lib/python3.9/site-packages/hmpps_person_match_score/model.json'

# runtime OS dependencies
RUN apt-get install -y libstdc++ \
    && rm -rf /var/lib/apt/lists/*

# copy the built virtual environment and entry point
COPY --from=build /venv /venv
RUN mkdir /venv/var
COPY docker-entrypoint.sh wsgi.py ./

# create app user
RUN groupadd -g 1001 appuser && \
    useradd -u 1001 -g appuser -m -s /bin/bash appuser

EXPOSE 5000

CMD ["./docker-entrypoint.sh"]
