#!/bin/bash
export FLASK_APP=matcher
export FLASK_ENV=development

#source $(pipenv --venv)/bin/activate
#flask run
poetry run flask run
