import os

import jwt
import requests
from authlib.jose import JsonWebKey
from cachetools import TTLCache

jwks_cache = TTLCache(maxsize=1, ttl=3600)


class JWKS:
    """
    JWKS class to be used to retrieve credentials
    """

    ALGORITHMS = ["RS256"]
    TIMEOUT = 300

    def __init__(self):
        self._jwk_url = self._get_jwk_url()

    def get_public_key_from_jwt(self, jwt_token):
        """
        Fetch the public key from the JWT token
        """
        unverified_header = jwt.get_unverified_header(jwt_token)
        kid = unverified_header.get("kid")

        jwks = self._get_jwks()

        for jwk in jwks:
            if jwk["kid"] == kid:
                return JsonWebKey.import_key(jwk)

        raise ValueError(f"Public key for kid: '{kid}' not found.")

    def _get_jwk_url(self):
        """
        Construct JWKS URL
        """
        return f"{self._get_env_var("OAUTH_BASE_URL")}/.well-known/jwks.json"

    def _get_jwks(self):
        """
        Get the keys from the JWKS endpoint
        """
        if "keys" not in jwks_cache:
            response = requests.get(self._jwk_url, timeout=self.TIMEOUT)
            response.raise_for_status()
            jwks_cache["keys"] = response.json()["keys"]
        return jwks_cache["keys"]

    @staticmethod
    def _get_env_var(key):
        """
        Helper function to retrieve an environment variable.
        """
        env_var = os.environ.get(key)
        if not env_var:
            raise ValueError(f"Missing environment variable: {key}")
        return env_var
