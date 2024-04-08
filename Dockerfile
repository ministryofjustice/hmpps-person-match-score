# syntax=docker/dockerfile:1
FROM python:3.9.18-slim-bullseye as base

# load in build details
ARG BUILD_NUMBER
ARG GIT_REF
ARG GIT_BRANCH

ENV APP_BUILD_NUMBER=${BUILD_NUMBER} \
    APP_GIT_REF=${GIT_REF} \
    APP_GIT_BRANCH=${GIT_BRANCH}

# Update pip
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.8.2 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

##############
# BUILD stage
##############
FROM base as build
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
# poetry suggested install, rather than using pip
RUN curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# install Python dependencies in virtual environment
RUN poetry install --no-dev

##############
# FINAL stage
##############
FROM base as final

# copy the built virtual environment and entry point
COPY --from=build $PYSETUP_PATH $PYSETUP_PATH

COPY ./hmpps_person_match_score /opt/hmpps_person_match_score/
COPY docker-entrypoint.sh wsgi.py /opt/

WORKDIR /opt/

ENV MODEL_PATH='/opt/hmpps_person_match_score/model.json'

# create app user
RUN groupadd -g 1001 appuser && \
    useradd -u 1001 -g appuser -m -s /bin/bash appuser
USER 1001

EXPOSE 5000

CMD ["./docker-entrypoint.sh"]
