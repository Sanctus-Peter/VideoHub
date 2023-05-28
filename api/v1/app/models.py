import uuid
from datetime import datetime
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from . import config, security, extractors

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
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(video_id={self.host_id}, host_service={self.host_service})"

    @staticmethod
    def add_video(url, user_id=None):
        """
        Adds a video to the database.

        Args:
            url (str): The URL of the video.
            user_id (UUID, optional): The ID of the user who added the video.

        Returns:
            Video: The created Video instance.

        Raises:
            Exception: If the user does not exist or if the video already exists.

        """
        host_id = extractors.extract_video_id(url)
        if host_id is None:
            return None
        if User.check_user_exists(user_id=user_id) is None:
            raise Exception("User not found")
        qry = Video.objects.filter(host_id=host_id, user_id=user_id.user_id).allow_filtering().first()
        if qry is None:
            raise Exception("Video already exists")
        return Video.create(host_id=host_id, user_id=user_id.user_id, url=url)
