import uuid
from datetime import datetime

from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from . import config, security, extractors
from .exceptions import (
    InvalidUserExceptions, VideoExistException, InvalidYoutubeVideoURLException
)
from api.v1.app.shortcuts import templates

settings = config.get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    firstname = columns.Text()
    lastname = columns.Text()
    password = columns.Text()
    created_at = columns.DateTime(primary_key=True, default=datetime.utcnow())

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"

    @staticmethod
    def create_user(email, firstname, lastname, password):
        """
        Creates a new User instance and saves it to the database.

        Args:
            email (str): The email address of the user.
            firstname (str): The first name of the user.
            lastname (str): The last name of the user.
            password (str): The user's password.

        Returns:
            User: The created User instance.

        """
        obj = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=security.hashed(password)
        )
        obj.save()
        return obj

    @staticmethod
    def check_user_exists(user_id):
        """
        Checks if a user with the specified user ID exists in the database.

        Args:
            user_id (UUID): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.

        """
        return User.objects.filter(user_id=user_id).allow_filtering() is not None

    @staticmethod
    def check_user_by_id(user_id=None):
        """
        Retrieves a user by their ID.

        Args:
            user_id (UUID): The ID of the user to retrieve.

        Returns:
            User or None: The User instance if found, None otherwise.

        """
        if user_id is None:
            return None

        return User.objects.filter(user_id=user_id).allow_filtering().first()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(Title={self.title}, video_id={self.host_id}, host_service={self.host_service})"

    @property
    def path(self):
        return f"/api/video/{self.host_id}"

    def as_data(self):
        return {f"{self.host_service}_id": self.host_id, "path": self.path}

    def render(self):
        basename = self.host_service
        template = f"videos/renders/{basename}.html"
        context = {
            "host_id": self.host_id
        }
        t = templates.get_template(template)
        return t.render(context)

    @staticmethod
    def add_video(url, user_id=None, title=None):
        """
        Adds a video to the database.

        Args:
            :param url: The URL of the video.
            :param user_id: user_id of the user
            :param title: title of the video

        Returns:
            Video: The created Video instance.

        Raises:
            Exception: If the user does not exist or if the video already exists.


        """
        host_id = extractors.extract_video_id(url)
        if host_id is None:
            raise InvalidYoutubeVideoURLException("Invalid Youtube Video URL")
        if User.check_user_exists(user_id) is None:
            raise InvalidUserExceptions("User not found")
        qry = Video.objects.filter(host_id=host_id).allow_filtering().first()
        if qry is not None:
            raise VideoExistException("Video already exists")
        return Video.create(host_id=host_id, user_id=user_id, url=url, title=title)


class WatchEvent(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    event_id = columns.TimeUUID(primary_key=True, clustering_order="DESC", default=uuid.uuid1)
    user_id = columns.UUID(primary_key=True)
    path = columns.Text()
    start_time = columns.Double()
    end_time = columns.Double()
    duration = columns.Double()
    complete = columns.Boolean(default=False)

    # def __str__(self):
    #     return self.__repr__()
    #
    # def __repr__(self):
    #     return f"WatchEvent(user_id={self.user_id}, video_id={self.video_id})"
    #
    # @staticmethod
    # def add_watch_event(user_id, video_id):
    #     """
    #     Adds a watch event to the database.
    #
    #     Args:
    #         user_id (UUID): The ID of the user.
    #         video_id (UUID): The ID of the video.
    #
    #     Returns:
    #         WatchEvent: The created WatchEvent instance.
    #
    #     """
    #     return WatchEvent.create(user_id=user_id, video_id=video_id)
