
install:
	poetry install

lint:
	poetry run ruff check hmpps_person_match_score/
	poetry run ruff check tests/
	

lint-fix:
	poetry run ruff check hmpps_person_match_score/ --fix

run:
	export FLASK_APP=hmpps_person_match_score; \
	export FLASK_ENV=development; \
	poetry run flask run

build:
	docker build . -t hmpps_person_match_score

test:
	poetry run pytest
