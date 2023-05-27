from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, SecretStr, root_validator
from api.v1.app import oauth2
from api.v1.app.models import User


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    lastname: str
    firstname: str
    password: SecretStr
    confirm_password: SecretStr

    @validator("email")
    def email_is_available(cls, v, values, **kwargs):
        if User.objects.filter(email=v):
            raise ValueError(f"User with {v} already exists")
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v


class UserLogin(UserBase):
    password: SecretStr
    session_id: str = None

    @root_validator
    def user_exists(cls, values):
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
    id: Optional[Any] = None
