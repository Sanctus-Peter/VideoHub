"""
This module provides authentication-related functions and classes for the FastAPI application.

It includes functionality for token generation, token verification, user authentication, and authentication backends.

Classes:
- JWTCookiePayload: Custom authentication backend that validates JWT tokens stored in cookies.

Functions:
- create_access_token: Generates an access token for a given user.
- verify_token: Verifies and decodes a JWT token.
- authenticate_user: Authenticates a user based on email and password.

Exceptions:
- credentials_exception: Represents an HTTP 401 Unauthorized exception for credential validation failures.

"""

from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from api.v1.app.config import get_settings
from api.v1.app.exceptions import HandleExceptions
from api.v1.app.models import User
from api.v1.app import security

settings = get_settings()
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


class JWTCookiePayload(AuthenticationBackend):
    """
    Authentication backend for JWT token stored in a cookie.

    """
    async def authenticate(self, request):
        """
        Authenticates the user based on the JWT token stored in the session_id cookie.

        Args:
            request: The request object.

        Returns:
            Tuple: A tuple containing the authentication credentials and the authenticated user.

        """
        session_id = request.cookies.get("session_id")
        user_data = verify_token(session_id, credentials_exception)
        if not user_data:
            return AuthCredentials(["anonymous"]), UnauthenticatedUser()
        user_id = user_data.get("user_id")
        return AuthCredentials(["authenticated"]), SimpleUser(user_id)


def create_access_token(user_obj: User):
    """
    Creates an access token for the given user.

    Args:
        user_obj: The User object for which the token is being created.

    Returns:
        str: The access token as a JWT string.

    """
    encode = {
        "user_id": str(user_obj.user_id),
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode["exp"] = expire

    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_token(token: str, credentialsException):
    """
    Verifies the authenticity and integrity of a JWT token.

    Args:
        token: The JWT token string to verify.
        credentialsException: The exception to raise if the verification fails.

    Returns:
        dict: The decoded payload of the token if it is valid.

    """
    payload = None
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            _id = payload.get("user_id")
            if not _id:
                raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)

        except JWTError:
            print("Logged out")
    return payload


def authenticate_user(email: str, password: str):
    """
    Authenticates a user based on their email and password.

    Args:
        email: The user's email.
        password: The user's password.

    Returns:
        User: The authenticated user object.

    Raises:
        HandleExceptions: If the user is not found or the password is incorrect.

    """
    user = User.objects.get(email=email)
    if not user:
        raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)
    if not security.verify(user.password, password):
        return None
    return user
