from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, SecretStr, root_validator
from api.v1.app import oauth2
from api.v1.app.models import User


class UserBase(BaseModel):
    """
    Base model for user data.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    lastname: str
    firstname: str
    password: SecretStr
    confirm_password: SecretStr

    @validator("email")
    def email_is_available(cls, v, values, **kwargs):
        """
        Validator to check if the provided email is available (not already used by an existing user).
        """
        if User.objects.filter(email=v):
            raise ValueError(f"User with {v} already exists")
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        """
        Validator to check if the provided password matches the confirm_password field.
        """
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserLogin(UserBase):
    """
    Model for user login.
    """
    password: SecretStr
    session_id: str = None

    @root_validator
    def user_exists(cls, values):
        """
        Root validator to check if the user exists and the provided credentials are correct.
        """
        email = values.get('email') or None
        password = values.get('password') or None

        if not email or not password:
            raise ValueError('incorrect credentials')

        password = password.get_secret_value()
        user = oauth2.authenticate_user(email, password)

        if not user:
            raise ValueError('incorrect credentials')

        token = oauth2.create_access_token(user)
        return {"session_id": token}


class TokData(BaseModel):
    """
    Model for token data.
    """
    id: Optional[Any] = None
