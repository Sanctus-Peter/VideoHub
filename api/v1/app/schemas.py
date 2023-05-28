import uuid
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, validator, SecretStr, root_validator
from api.v1.app import oauth2
from api.v1.app.models import User, Video
from api.v1.app.extractors import extract_video_id
from .exceptions import (
    InvalidUserExceptions, VideoExistException, InvalidYoutubeVideoURLException
)


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


class VideoCreate(BaseModel):
    """
    Model for creating a video.

    Attributes:
        url (str): The URL of the video.
        user_id (str): The ID of the user who is adding the video.

    """
    url: str
    user_id: str
    title: str

    @validator('url')
    def validate_url(cls, v, values, **kwargs):
        """
            Validator to check if the provided URL is a valid YouTube video URL.

            Args:
                v (str): The URL value.
                values (dict): The values of other fields in the model.
                **kwargs: Additional arguments.

            Returns:
                str: The validated URL.

            Raises:
                ValueError: If the URL is not a valid YouTube video URL.

        """
        video_id = extract_video_id(v)
        if not video_id:
            raise ValueError(f'{v} is not a valid youtube video url')
        return v

    @root_validator
    def validate_data(cls, values):
        """
            Root validator to validate the video data.

            Args:
                values (dict): The values of the model attributes.

            Returns:
                dict: The validated video data.

            Raises:
                ValueError: If there is an error with the account, the video URL is invalid,
                    the video already exists, or there is a general error.

        """
        url = values.get('url')
        user_id = values.get('user_id')
        title = values.get('title')
        video_object = None
        try:
            video_object = Video.add_video(url=url, user_id=user_id, title=title)
        except InvalidUserExceptions:
            raise ValueError("There is an error with your account, please try again")
        except InvalidYoutubeVideoURLException:
            raise ValueError(f"{url} is not a valid youtube video url")
        except VideoExistException:
            raise ValueError(f"{url} already exists")
        except Exception as e:
            raise ValueError("There is an error with your account, please try again")
        if not video_object:
            raise ValueError("There is an error with your account, please try again")
        if not isinstance(video_object, Video):
            raise ValueError("There is an error with your account, please try again")
        return video_object.as_data()


class WatchEvent(BaseModel):
    host_id: str
    start_time: float
    end_time: float
    duration: float
    complete: bool
    path: Optional[str]


class TokData(BaseModel):
    """
    Model for token data.
    """
    id: Optional[Any] = None
