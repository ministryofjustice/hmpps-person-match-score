import pytest

from hmpps_person_match_score.app import MatchScoreFlaskApplication


@pytest.fixture(scope="module")
def app():
    app = MatchScoreFlaskApplication().app
    app.config.update(
        {
            "TESTING": True,
        },
    )
    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()
