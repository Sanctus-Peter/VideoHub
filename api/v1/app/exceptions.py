from fastapi import HTTPException


class HandleExceptions(HTTPException):
    pass


class InvalidYoutubeVideoURLException(Exception):
    pass


class VideoExistException(Exception):
    pass


class InvalidUserExceptions(Exception):
    pass
