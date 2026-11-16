"""Small checks used by every service."""

from app.exceptions import InvalidDataError
from app.models.database import get_rows


def check_text(value, label):
    value = value.strip()
    if value == "":
        raise InvalidDataError(label + " cannot be empty.")
    return value


def check_choice(value, choices, label):
    if value not in choices:
        raise InvalidDataError(label + " must be one of: " + ", ".join(choices))


def check_quantity(quantity):
    if quantity <= 0:
        raise InvalidDataError("Quantity must be greater than zero.")


def make_id(prefix, wanted_id, table, column):
    """Use the typed ID (it must be new) or create the next one like DON-013."""
    existing_ids = set()  # a set makes the duplicate check easy
    for row in get_rows("SELECT " + column + " FROM " + table):
        existing_ids.add(row[0])

    wanted_id = wanted_id.strip().upper()
    if wanted_id != "":
        if wanted_id in existing_ids:
            raise InvalidDataError("ID " + wanted_id + " already exists.")
        return wanted_id

    number = len(existing_ids) + 1
    while prefix + "-" + str(number).zfill(3) in existing_ids:
        number += 1
    return prefix + "-" + str(number).zfill(3)
