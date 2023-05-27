from fastapi import Request, HTTPException, status
from functools import wraps
from api.v1.app.exceptions import HandleExceptions
from api.v1.app.oauth2 import verify_token


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def login_required(func):
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)
    return wrapper
