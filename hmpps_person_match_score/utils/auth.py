from functools import wraps

import jwt
from flask import abort, request

from hmpps_person_match_score.utils.jwks import JWKS


def authorize(required_roles: list[str]):
    """
    Decorator to enforce role-based access control.
    Args:
        required_roles (List[str]): List of roles required to access the decorated function.
    Returns:
        Callable: Decorated function that requires authorization.
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get the JWT from the Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                abort(401, description="Authorization token is missing or invalid.")

            token = auth_header.split(" ")[1]

            try:
                # Fetch the public key based on the 'kid' in the JWT header
                public_key = JWKS().get_public_key_from_jwt(token)

                # Decode and validate the JWT with the public key
                payload = jwt.decode(token, public_key, algorithms=JWKS.ALGORITHMS, audience="your_audience_here")

                # Check if the required role is in the JWT's roles claim
                user_roles = payload.get("authorities", [])
                if required_roles not in user_roles:
                    abort(403, description="You do not have permission to access this resource.")
                return f(*args, **kwargs)

            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValueError):
                abort(401, description="Invalid or expired token.")

            return decorated_function

        return decorator
