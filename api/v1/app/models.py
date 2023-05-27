import uuid
from datetime import datetime
from cassandra.cqlengine.models import Model
from cassandra.cqlengine import columns
from . import config, utils, security

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
        obj = User(
            email=email,
            firstname=firstname,
            lastname=lastname,
            password=security.hashed(password)
        )
        obj.save()
        return obj
