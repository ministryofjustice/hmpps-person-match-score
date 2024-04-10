from hmpps_person_match_score.views.ping_view import PingView


class TestPingView:
    """
    Test ping view
    """

    def test_response_ok(self, client):
        """
        Test a get to the health endpoint returns a 200 ok
        """
        response = client.get(PingView.ROUTE)
        assert response.status_code == 200
        assert response.text == "pong"
