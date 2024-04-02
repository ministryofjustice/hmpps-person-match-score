import pytest

from hmpps_person_match_score.app import MatchScoreFlaskApplication


@pytest.fixture()
def app():
    app = MatchScoreFlaskApplication().app
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_match(client):
    response = client.post("/match", json=valid_sample)
    # Note: no Bayes Factors asserted - match probability should be sufficient
    assert response is not None
    assert response.status_code == 200
    assert response.json["match_probability"]["0"] == 0.999353426
    assert response.json["source_dataset_l"]["0"] == "delius"
    assert response.json["unique_id_l"]["0"] == "862"
    assert response.json["source_dataset_r"]["0"] == "libra"
    assert response.json["unique_id_r"]["0"] == "861"
    assert response.json["surname_std_l"]["0"] == "robibnson"
    assert response.json["surname_std_r"]["0"] == "robinson"
    assert response.json["forename1_std_l"]["0"] == "lily"
    assert response.json["forename1_std_r"]["0"] == "lily"
    assert response.json["forename2_std_l"]["0"] is None
    assert response.json["forename2_std_r"]["0"] is None
    assert response.json["forename3_std_l"]["0"] is None
    assert response.json["forename3_std_r"]["0"] is None
    assert response.json["gamma_surname_std"]["0"] == 1
    assert response.json["gamma_forename1_std"]["0"] == 2
    assert response.json["gamma_forename2_std"]["0"] == -1
    assert response.json["gamma_forename3_std"]["0"] == -1
    assert response.json["dob_std_l"]["0"] == "2009-07-06"
    assert response.json["dob_std_r"]["0"] == "2009-07-06"
    assert response.json["gamma_dob_std"]["0"] == 4
    assert response.json["pnc_number_std_l"]["0"] is None
    assert response.json["pnc_number_std_r"]["0"] == "2001/0141640Y"
    assert response.json["gamma_pnc_number_std"]["0"] == -1


def test_health(client):
    response = client.get("/health")
    assert response is not None
    assert response.status_code == 200


valid_sample = {
    "unique_id": {"0": "861", "1": "862"},
    "first_name": {"0": "Lily", "1": "Lily"},
    "surname": {"0": "Robinson", "1": "Robibnson"},
    "dob": {"0": "2009-07-06", "1": "2009-07-06"},
    "pnc_number": {
        "0": "2001/0141640Y",
        "1": None,
    },
    "source_dataset": {"0": "libra", "1": "delius"},
}
