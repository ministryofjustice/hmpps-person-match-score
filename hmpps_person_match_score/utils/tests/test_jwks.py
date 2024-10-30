import os

import pytest
import requests

from hmpps_person_match_score.utils.jwks import JWKS


class TestJwks:
    """
    Test JWKS class
    """

    def test_retrieves_jwks(self, jwt_token_factory, mock_jwks):
        """
        Test the JWKS class using a mock JWKS endpoint
        """
        token = jwt_token_factory(roles=["test_role"])
        public_key = JWKS().get_public_key_from_jwt(token)
        assert public_key is not None

    def test_missing_oauth_env_var_throws_error(self):
        """
        Test that an error is raised when the OAUTH_BASE_URL environment variable is missing
        """
        os.environ.pop("OAUTH_BASE_URL", None)
        with pytest.raises(ValueError) as e:
            JWKS()
        assert str(e.value) == "Missing environment variable: OAUTH_BASE_URL"

    def test_raises_error_no_key_found(self, jwt_token_factory, mock_jwks):
        """
        Test that an error is raised when a public key for a specific kid is not found
        """
        token = jwt_token_factory(kid="invalid_kid")
        with pytest.raises(ValueError) as e:
            JWKS().get_public_key_from_jwt(token)
        assert str(e.value) == "Public key for kid: 'invalid_kid' not found."

    def test_raises_error_on_error_response_from_jwks_endpoint(self, jwt_token_factory, mock_jwks_call_factory):
        """
        Test that an error is raised when the JWKS endpoint returns an error response
        """
        mock_jwks_call_factory(status_code=500)
        token = jwt_token_factory()
        with pytest.raises(requests.exceptions.HTTPError):
            JWKS().get_public_key_from_jwt(token)
