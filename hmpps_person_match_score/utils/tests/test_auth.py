from http import HTTPStatus

from flask import Response

from hmpps_person_match_score.utils.auth import authorize


class TestAuth:
    """
    Test Auth class
    """

    TEST_ROLE = "ROLE_TEST"

    @authorize(required_roles=[TEST_ROLE])
    def method_with_single_role(self):
        return Response(status=HTTPStatus.OK)

    def test_allows_correct_level_of_auth(self, app, jwt_token_factory, mock_jwks):
        """
        Test that method with single role is accessible when authenticated with correct role
        """
        token = jwt_token_factory(roles=[self.TEST_ROLE])
        token_header = { "Authorization": f"Bearer {token}" }
        with app.test_request_context(headers=token_header):
            response = self.method_with_single_role()
            assert response.status_code == HTTPStatus.OK
