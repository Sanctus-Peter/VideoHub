from algoliasearch.search_client import SearchClient

from api.v1.app import config
from api.v1.app.models import Playlist, Video
from api.v1.app.schemas import VideoIndex, PlaylistIndex

settings = config.get_settings()

ALGOLIA_INDEX_NAME = settings.algolia_index_name
ALGOLIA_APP_ID = settings.algolia_app_id
ALGOLIA_API_KEY = settings.algolia_api_key


def get_index(name=ALGOLIA_INDEX_NAME):
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    index = client.init_index(name)
    return index


def get_data_set():
    playlist_qry = [dict(x) for x in Playlist.objects.all()]
    playlist_data_set = [PlaylistIndex(**x).dict() for x in playlist_qry]
    video_qry = [dict(x) for x in Video.objects.all()]
    video_dataset = [VideoIndex(**x).dict() for x in video_qry]

    return playlist_data_set + video_dataset


def update_index():
    index = get_index()
    dataset = get_data_set()
    index_response = index.save_objects(dataset).wait()
    try:
        len_index = len(list(index_response)[0]["objectIDs"])
    except Exception as e:
        len_index = None
    return len_index


def search_index(query):
    index = get_index()
    return index.search(query)
