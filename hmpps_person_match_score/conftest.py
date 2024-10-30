import datetime
import os
from unittest.mock import patch

import jwt
import pytest
from authlib.jose import JsonWebKey
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(autouse=True)
def disable_cache():
    with patch("hmpps_person_match_score.utils.jwks.jwks_cache", {}):
        yield


@pytest.fixture
def context():
    """
    Returns Test context to use through app
    """

    class TestContext:
        DEFAULT_KID = "test_kid"

        def __init__(self):
            self.kid = self.DEFAULT_KID

    return TestContext()


@pytest.fixture(autouse=True)
def set_env_vars():
    os.environ["APP_BUILD_NUMBER"] = "number"
    os.environ["APP_GIT_REF"] = "ref"
    os.environ["APP_GIT_BRANCH"] = "branch"
    os.environ["OAUTH_BASE_URL"] = "http://localhost:5000"


@pytest.fixture
def private_key():
    """
    Returns a generated private key for testing purposes.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key


@pytest.fixture
def public_key(private_key):
    """
    Returns the public key from the private key for testing purposes.
    """
    public_key = private_key.public_key()
    return public_key


@pytest.fixture
def jwks(context, public_key):
    """
    Return a JWKS for testing purposes
    """
    jwk = JsonWebKey.import_key(
        public_key,
        {
            "kty": "RSA",
            "kid": context.kid,
        },
    )
    jwks = {"keys": [jwk.as_dict()]}
    return jwks


@pytest.fixture
def jwt_token_factory(context, private_key):
    """
    Returns a JWT token for testing purposes
    """

    def _create_token(
        kid: str = context.kid,
        roles: list[str] = None,
        expiry: datetime.timedelta = datetime.timedelta(hours=1),
    ):
        if roles is None:
            roles = []

        headers = {"kid": kid}
        payload = {
            "authorities": roles,
            "exp": datetime.datetime.now() + expiry,
            "iss": "test_issuer",
            "aud": "test_audience",
        }
        token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
        return token

    return _create_token


@pytest.fixture
def mock_jwks_call_factory(jwks, requests_mock):
    """
    Returns a func to create a mock request to JWKS endpoint.
    """

    def _mock_jwks_call(status_code: int = 200, headers: dict = None, json_data: dict = None):
        """
        Mock call to JWKS endpoint.
        """
        url = f"{os.environ.get("OAUTH_BASE_URL")}/.well-known/jwks.json"

        if headers is None:
            headers = {"Content-Type": "application/json"}
        if json_data is None:
            json_data = jwks

        requests_mock.get(url, headers=headers, json=json_data, status_code=status_code)

    return _mock_jwks_call


@pytest.fixture()
def mock_jwks(mock_jwks_call_factory, jwks):
    """
    Returns a mock JWKS with public key generated.
    """
    default_response_json = jwks
    mock_jwks_call_factory(json_data=default_response_json)
