"""Custom errors. Each one has an HTTP status code that main.py sends back to the frontend."""


class FoodBridgeError(Exception):
    status_code = 400


class NotFoundError(FoodBridgeError):
    """A donation, recipient or distribution does not exist."""
    status_code = 404


class InvalidDataError(FoodBridgeError):
    """Wrong input: empty text, bad quantity, duplicate ID, not enough food ..."""
    status_code = 400


class DatabaseError(FoodBridgeError):
    """The SQLite database could not be read or written."""
    status_code = 500
