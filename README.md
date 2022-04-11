# HMPPS Person Match Score API

An API wrapper around a model developed by the MoJ Analytical Platform for scoring the confidence 
of people matches across MoJ systems.

## Pre-Requisites

* Python 3.8+
* [Poetry](https://python-poetry.org/docs/)

## Install

Install using poetry

`poetry install`

## Run

`./run.sh`

## Test

`poetry run pytest`

## Dev

Developed using [PyCharm](https://www.jetbrains.com/pycharm/download/)

### Update Requirements File

`poetry export --without-hashes -f requirements.txt --output requirements.txt`

## TODO

- unit tests
- ping & health check for k8s liveness and readiness probes
- instrument
- app insights custom events
- improve database table management
- package
- dockerfile
- helm
- CI/CD

## Notes

* Ported from a [PoC using AWS Lambda](https://github.com/moj-analytical-services/pic_scoring_prototype_python)
* [Tutorial for Flask](https://flask.palletsprojects.com/en/2.1.x/tutorial/)