import datetime
import json
import os

import jwt
import pytest
from authlib.jose import JsonWebKey
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@pytest.fixture(autouse=True, scope="session")
def set_env_vars():
    os.environ["APP_BUILD_NUMBER"] = "number"
    os.environ["APP_GIT_REF"] = "ref"
    os.environ["APP_GIT_BRANCH"] = "branch"
    os.environ["OAUTH_BASE_URL"] = "http://localhost:5000"


@pytest.fixture
def private_key_credentails():
    """
    Returns a generated private key for testing purposes.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return private_key, private_pem

@pytest.fixture
def public_key_credentails(private_key_credentails):
    """
    Returns the public key from the private key for testing purposes.
    """
    private_key, private_key_pem = private_key_credentails
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return public_key, public_pem


@pytest.fixture
def jwks(public_key):
    """
    Return a JWKS for testing purposes
    """
    jwk = JsonWebKey(public_key, {"kty": "RSA"})
    jwks = {"keys": [jwk.as_dict()]}
    return json.dumps(jwks.dumps(jwk, indent=2))


@pytest.fixture
def jwt_token_factory(private_key_credentails):
    """
    Returns a JWT token for testing purposes
    """
    private_key, private_key_pem = private_key_credentails

    def _create_token(kid: str, roles: list[str] = None, expiry: datetime.timedelta = datetime.timedelta(hours=1)):
        if roles is None:
            roles = []

        headers = {"kid": kid}
        payload = {
            "authorities": roles,
            "exp": datetime.datetime.utcnow() + expiry,
            "iss": "test_issuer",
            "aud": "test_audience",
        }
        token = jwt.encode(payload, private_key, algorithm="RS256", headers=headers)
        return token

    return _create_token
