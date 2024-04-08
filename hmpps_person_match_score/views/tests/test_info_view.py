from hmpps_person_match_score.views.info_view import InfoView


class TestInfoView:
    """
    Test info view
    """

    def test_response_ok(self, client):
        """
        Test a get to the info endpoint returns a 200 ok
        """
        response = client.get(InfoView.ROUTE)
        assert response is not None
        assert response.headers.get("Content-Type") == "application/json"
        assert response.status_code == 200
        assert response.json["version"] == "number"
        assert response.json["commit_id"] == "ref"
        assert response.json["branch"] == "branch"
