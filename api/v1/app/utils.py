import json
from pydantic.error_wrappers import ValidationError


def valid_schema_data(schema, rw_data: dict):
    """
    Validates the raw data against the provided Pydantic schema.

    Args:
        schema: The Pydantic schema to validate against.
        rw_data: A dictionary of raw data to be validated.

    Returns:
        A tuple containing the validated data and a list of validation errors.
        The validated data is a dictionary containing the validated values.
        The validation errors are a list of dictionaries, where each dictionary represents an error and contains the
        following keys: 'loc' (location of the error), 'msg' (error message), and 'type' (type of error).

    """
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
