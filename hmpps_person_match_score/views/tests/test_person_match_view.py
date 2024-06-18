import pytest

from hmpps_person_match_score.views.person_match_view import PersonMatchView


class TestPersonMatchView:
    """
    Test match view
    """

    @pytest.fixture(autouse=True)
    def test_context(self):
        self.valid_sample = {
            "matching_from": {
                "unique_id": "1",
                "firstname1": "Lily",
                "lastname": "Robinson",
                "dob": "2009-07-06",
                "pnc": "2001/0141640Y",
            },
            "matching_to": [
                {
                    "unique_id": "2",
                    "firstname1": "Lily",
                    "lastname": "Robibnson",
                    "dob": "2009-07-06",
                    "pnc": None,
                },
            ],
        }
        self.exact_match = {
            "matching_from": {
                "unique_id": "1",
                "firstname1": "Jane",
                "lastname": "Smith",
                "dob": "2009-07-06",
                "pnc": "2001/0141640Y",
            },
            "matching_to": [
                {
                    "unique_id": "2",
                    "firstname1": "Jane",
                    "lastname": "Smith",
                    "dob": "2009-07-06",
                    "pnc": "2001/0141640Y",
                },
            ],
        }

    def test_complete_message(self, client):
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert response.json["match_probability"]["0"] == 0.999353426
        assert response.json["source_dataset_l"]["0"] == "matching_from"
        assert response.json["unique_id_l"]["0"] == "1"
        assert response.json["source_dataset_r"]["0"] == "matching_to"
        assert response.json["unique_id_r"]["0"] == "2"
        assert response.json["lastname_l"]["0"] == "Robinson"
        assert response.json["lastname_r"]["0"] == "Robibnson"
        assert response.json["firstname1_l"]["0"] == "Lily"
        assert response.json["firstname1_r"]["0"] == "Lily"
        assert response.json["firstname2_l"]["0"] is None
        assert response.json["firstname2_r"]["0"] is None
        assert response.json["firstname3_l"]["0"] is None
        assert response.json["firstname3_r"]["0"] is None
        assert response.json["gamma_lastname"]["0"] == 1
        assert response.json["gamma_firstname1"]["0"] == 2
        assert response.json["gamma_firstname2"]["0"] == -1
        assert response.json["gamma_firstname3"]["0"] == -1
        assert response.json["dob_l"]["0"] == "2009-07-06"
        assert response.json["dob_r"]["0"] == "2009-07-06"
        assert response.json["gamma_dob"]["0"] == 4
        assert response.json["pnc_l"]["0"] == "2001/0141640Y"
        assert response.json["pnc_r"]["0"] is None
        assert response.json["gamma_pnc"]["0"] == -1

    def test_fuzzy_match_on_first_name(self, client):
        self.exact_match["matching_to"][0]["firstname1"] = "Jayne"
        response = client.post(PersonMatchView.ROUTE, json=self.exact_match)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert response.json["match_probability"]["0"] == 0.9999999001
        assert response.json["firstname1_l"]["0"] == "Jane"
        assert response.json["firstname1_r"]["0"] == "Jayne"

    def test_fuzzy_match_on_last_name(self, client):
        self.exact_match["matching_to"][0]["lastname"] = "Smythe"
        response = client.post(PersonMatchView.ROUTE, json=self.exact_match)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert response.json["match_probability"]["0"] == 0.9999997925
        assert response.json["lastname_l"]["0"] == "Smith"
        assert response.json["lastname_r"]["0"] == "Smythe"

    def test_fuzzy_match_on_pnc(self, client):
        self.exact_match["matching_to"][0]["pnc"] = "2003/0141640Y"
        response = client.post(PersonMatchView.ROUTE, json=self.exact_match)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert response.json["match_probability"]["0"] == 0.999999481
        assert response.json["pnc_l"]["0"] == "2001/0141640Y"
        assert response.json["pnc_r"]["0"] == "2003/0141640Y"

    def test_fuzzy_match_on_dob(self, client):
        self.exact_match["matching_to"][0]["dob"] = "2009-08-07"
        response = client.post(PersonMatchView.ROUTE, json=self.exact_match)
        assert response.status_code == 200
        assert response.headers.get("Content-Type") == "application/json"
        assert response.json["match_probability"]["0"] == 0.999989593
        assert response.json["dob_l"]["0"] == "2009-07-06"
        assert response.json["dob_r"]["0"] == "2009-08-07"

    def test_handles_multiple_records(self, client):
        multiple_records = [
            {
                "unique_id": f"{i}",
                "firstname1": "Lily",
                "lastname": "Robibnson",
                "dob": "2009-07-06",
                "pnc": None,
            }
            for i in range(1, 20)
        ]
        self.valid_sample["matching_to"] = multiple_records
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 200
        assert len(response.json["match_probability"]) == 19
        assert all([x == 0.999353426 for x in response.json["match_probability"].values()])

    def test_validation_error_no_matching_to(self, client):
        del self.valid_sample["matching_to"]
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 400

    def test_validation_error_no_matching_from(self, client):
        del self.valid_sample["matching_from"]
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 400

    def test_validation_error_not_as_list(self, client):
        self.valid_sample["matching_to"] = {
            "firstname1": "Lily",
            "lastname": "Robinson",
            "dob": "2009-07-06",
            "pnc": "2001/0141640Y",
        }
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 400
