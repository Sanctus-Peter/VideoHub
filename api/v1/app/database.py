import pathlib
from cassandra.cluster import Cluster, TokenAwarePolicy, DCAwareRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
from . import config

BASE_DIR = pathlib.Path(__file__).resolve().parent

ASTRADB_CONNECT_BUNDLE = BASE_DIR / "unencrypted" / "astradb_connect.zip"

settings = config.get_settings()

ASTRADB_CLIENT_ID = settings.db_client_id
ASTRADB_CLIENT_SECRET = settings.db_client_secret


def get_session():
    """
    Establishes a connection to a Cassandra database and returns the session object.

    Returns:
        cassandra.cluster.Session: A session object for executing queries against the Cassandra database.
    """
    cloud_config = {
        'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    return session
