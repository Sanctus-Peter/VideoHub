import json
from pydantic.error_wrappers import ValidationError


def valid_schema_data(schema, rw_data: dict):
    data = {}
    errors = []
    try:
        user_data = schema(**rw_data)
        data = user_data.dict()

    except ValidationError as e:
        error_messages = e.json()
        try:
            errors = json.loads(error_messages)
        except json.JSONDecodeError as e:
            errors = [{"loc": "non_field_error", "msg": "An error occurred", "type": "server_error"}]
    return data, errors
