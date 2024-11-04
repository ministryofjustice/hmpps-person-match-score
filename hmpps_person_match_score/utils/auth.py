import datetime
import json
import logging
from functools import wraps
from http import HTTPStatus

import jwt
from flask import Response, request

from hmpps_person_match_score.utils.environment import EnvVars, get_env_var
from hmpps_person_match_score.utils.jwks import JWKS

logger = logging.getLogger("hmpps-person-match-score-logger")


def authorize(required_roles: list[str] = None):
    """
    Decorator to enforce role-based access control.
    Args:
        required_roles (List[str]): List of roles required to access the decorated function.
    Returns:
        Callable: Decorated function that requires authorization.
    """
    if required_roles is None:
        required_roles = []

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the JWT from the Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return _return_auth_error(HTTPStatus.UNAUTHORIZED, "Authorization token is missing or invalid.")

            token = auth_header.split(" ")[1]

            try:
                # Fetch the public key based on the 'kid' in the JWT header
                public_key = JWKS().get_public_key_from_jwt(token)
                pem_key = public_key.as_pem(is_private=False)

                # Decode and validate the JWT with the public key
                payload = jwt.decode(
                    token,
                    pem_key,
                    algorithms=JWKS.ALGORITHMS,
                    issuer=f"{get_env_var(EnvVars.OAUTH_BASE_URL_KEY)}/auth/issuer",
                )

                # Check if the required role is in the JWT's roles claim
                user_roles = payload.get("authorities", [])
                if not set(required_roles).issubset(user_roles):
                    return _return_auth_error(
                        HTTPStatus.FORBIDDEN, "You do not have permission to access this resource.",
                    )
                return f(*args, **kwargs)

            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
                return _return_auth_error(HTTPStatus.UNAUTHORIZED, "Invalid or expired token.")

        def _return_auth_error(status: HTTPStatus, error_message: str) -> Response:
            log_message = f"Authentication Error: {status} {error_message}"
            logger.error(log_message)
            return Response(
                status=status,
                mimetype="application/json",
                response=json.dumps(
                    {
                        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                        "error_message": error_message,
                        "status_code": status,
                    },
                ),
            )

        return decorated_function

    return decorator
