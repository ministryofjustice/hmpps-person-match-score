import os

import pytest

from hmpps_person_match_score.utils.jwks import JWKS


class TestJwks:
    """
    Test JWKS class
    """

    def test_missing_oauth_url_throws_error(self, jwt_token_factory):
        """
        Test that an error is raised when the oauth_base_url is missing
        """
        token = jwt_token_factory(kid="test1", roles=["test_role"])
        assert token is not None

    def test_missing_oauth_env_var_throws_error(self):
        """
        Test that an error is raised when the OAUTH_BASE_URL environment variable is missing
        """
        os.environ.pop("OAUTH_BASE_URL", None)
        with pytest.raises(ValueError) as e:
            JWKS()
        assert str(e.value) == "Missing environment variable: OAUTH_BASE_URL"
