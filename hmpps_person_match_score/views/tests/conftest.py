import os

import pytest

from hmpps_person_match_score.app import MatchScoreFlaskApplication


def pytest_generate_tests(metafunc):
    os.environ["APP_BUILD_NUMBER"] = "number"
    os.environ["APP_GIT_REF"] = "ref"
    os.environ["APP_GIT_BRANCH"] = "branch"
    os.environ["OAUTH_BASE_URL"] = "http://localhost:5000"


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
