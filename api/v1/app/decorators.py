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
    """
    Decorator to enforce authentication for API endpoints.

    This decorator checks if the user is authenticated by inspecting the `request.user.is_authenticated` attribute.
    If the user is not authenticated, it raises an HTTPException with the status code 401 Unauthorized.
    Otherwise, it allows the execution of the decorated function.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The decorated function.

    """
    @wraps(func)
    def wrapper(request: Request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise HandleExceptions(status_code=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)
    return wrapper
