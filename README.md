# HMPPS Person Match Score API

An API wrapper around a model developed by the MoJ Analytical Platform for scoring the confidence 
of people matches across MoJ systems.

## Pre-Requisites

* Python 3.8+
* Java JDK 11
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

## TODO - PiC

- health check for k8s liveness and readiness probes
- override flask SECRET_KEY
- instrument
- app insights custom events
- unit tests for web api wrapper
- helm
- CI/CD

### TODO - Panagiotis
- change from embedded DB to PySpark
- unit tests for data science functions
- change input/output to JSON
- (later) move to stand-alone Splink

## Notes

* Ported from a [PoC using AWS Lambda](https://github.com/moj-analytical-services/pic_scoring_prototype_python)
* [Tutorial for Flask](https://flask.palletsprojects.com/en/2.1.x/tutorial/)

```
curl -i \
    -H "Content-Type: application/json" \
    -X POST -d "{"unique_id":{"0":"861","1":"862"},"first_name":{"0":"Lily","1":"Lily"},"surname":{"0":"Robinson","1":"Robibnson"},"dob":{"0":"2009-07-06","1":"2009-07-06"},"pnc_number":{"0":"2001/0141640Y","1":"None"},"source_dataset":{"0":"libra","1":"delius"}}" \
    http://127.0.0.1:5000/match
```

To add an old version of splink to poetry that is not directly available:

`poetry add git+https://github.com/moj-analytical-services/splink.git#v1.0.6`
