import jwt
import requests
from authlib.jose import JsonWebKey
from cachetools import TTLCache
from requests import exceptions as rq_ex

from hmpps_person_match_score.utils.environment import EnvVars, get_env_var
from hmpps_person_match_score.utils.retry import RetryExecutor

jwks_cache = TTLCache(maxsize=1, ttl=3600)


class JWKS:
    """
    JWKS class to be used to retrieve credentials
    """

    ALGORITHMS = ["RS256"]
    TIMEOUT = 30

    RETRY_EXCEPTIONS = (
        rq_ex.Timeout,
        rq_ex.ConnectionError,
        rq_ex.HTTPError,
    )

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

    @staticmethod
    def _get_jwk_url():
        """
        Construct JWKS URL
        """
        return f"{get_env_var(EnvVars.OAUTH_BASE_URL_KEY)}/auth/.well-known/jwks.json"

    def _call_jwks_endpoint(self):
        """
        Call JWKS endpoint
        raise exception if failed to call endpoint
        """
        response = requests.get(self._jwk_url, timeout=self.TIMEOUT)
        response.raise_for_status()
        return response

    def _get_jwks(self):
        """
        Get the keys from the JWKS endpoint
        """
        if "keys" not in jwks_cache:
            response = RetryExecutor.retry(self._call_jwks_endpoint, retry_exceptions=self.RETRY_EXCEPTIONS)
            jwks_cache["keys"] = response.json()["keys"]
        return jwks_cache["keys"]
