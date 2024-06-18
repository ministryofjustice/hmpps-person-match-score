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
                "first_name": "Lily",
                "surname": "Robinson",
                "dob": "2009-07-06",
                "pnc_number": "2001/0141640Y",
            },
            "matching_to": [
                {
                    "first_name": "Lily",
                    "surname": "Robinson",
                    "dob": "2009-07-06",
                    "pnc_number": "2001/0141640Y",
                },
            ],
        }

    def test_validation_complete_message(self, client):
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 200

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
            "first_name": "Lily",
            "surname": "Robinson",
            "dob": "2009-07-06",
            "pnc_number": "2001/0141640Y",
        }
        response = client.post(PersonMatchView.ROUTE, json=self.valid_sample)
        assert response.status_code == 400

