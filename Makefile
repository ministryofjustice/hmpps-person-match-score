export PYTHONDONTWRITEBYTECODE=1

install:
	poetry install

lint:
	poetry run ruff check hmpps_person_match_score/
	
lint-fix:
	poetry run ruff check hmpps_person_match_score/ --fix

format:
	poetry run ruff format 

run:
	export FLASK_APP=hmpps_person_match_score; \
	export FLASK_ENV=development; \
	poetry run python hmpps_person_match_score/app.py

build:
	docker build . --tag hmpps_person_match_score \
		--build-arg BUILD_NUMBER="local" \
		--build-arg GIT_REF=$(shell git rev-parse --short HEAD) \
		--build-arg GIT_BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

run-docker:
	docker run -p 5000:5000 -t hmpps_person_match_score

test:
	poetry run pytest -v

test-ci:
	poetry run pytest --junitxml=test_results/pytest-report.xml
