## Pre-Requisites

* Python 3.x
* [Poetry](https://python-poetry.org/docs/)

## Install

Install using poetry

`poetry install`

Initialise the database

`./init-db.sh`

## Test

`poetry run pytest`

## Run

`./run.sh`

## Update Requirements File

`poetry export --without-hashes -f requirements.txt --output requirements.txt`

## TODO

- better URL path
- unit tests
- ping & health check
- instrument
- app insights custom events
- auto init DB
- improve database table management
- package
- dockerfile
- helm
- CI/CD


## Notes

https://python-poetry.org/docs/

Followed this tutorial for Flask:

https://flask.palletsprojects.com/en/2.1.x/tutorial/