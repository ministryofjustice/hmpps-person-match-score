from hmpps_person_match_score.views.health_view import HealthView


class TestHealthView:
    """
    Test health view
    """

    def test_response_ok(self, client):
        """
        Test a get to the health endpoint returns a 200 ok
        """
        response = client.get(HealthView.ROUTE)
        assert response.status_code == 200
        assert response.text == "UP"
