#!/bin/bash
export FLASK_APP=matcher
export FLASK_ENV=development

#source $(pipenv --venv)/bin/activate
#flask init-db
poetry run flask init-db
