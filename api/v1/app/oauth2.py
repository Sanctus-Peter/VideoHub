from starlette.authentication import (
    AuthenticationBackend,
    SimpleUser,
    UnauthenticatedUser,
    AuthCredentials
)

from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException
from .config import get_settings
from .exceptions import HandleExceptions
from .models import User

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
    async def authenticate(self, request):
        session_id = request.cookies.get("session_id")
        user_data = verify_token(session_id, credentials_exception)
        if not user_data:
            return AuthCredentials(["anonymous"]), UnauthenticatedUser()
        user_id = user_data.get("user_id")
        return AuthCredentials(["authenticated"]), SimpleUser(user_id)


def create_access_token(user_obj: User):
    encode = {
        "user_id": str(user_obj.user_id),
    }
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode["exp"] = expire

    encoded = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verify_token(token: str, credentialsException):
    payload = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        _id = payload.get("user_id")
        if not _id:
            raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)

    except JWTError:
        print("Logged out")
    return payload


def authenticate_user(email: str, password: str):
    user = User.objects.get(email=email)
    if not user:
        raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)
        # raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="You are not authorized to execute this action"
        # )
    # if not user.check_password(password):
    #     return False
    return user
