"""Recipient logic: get, search, add, update, delete."""

from app.exceptions import InvalidDataError, NotFoundError
from app.models.choices import RECIPIENT_TYPES
from app.models.database import run, get_rows
from app.models.recipient import Recipient
from app.services.validation import check_text, check_choice, make_id


def get_recipient(recipient_id):
    rows = get_rows("SELECT * FROM recipients WHERE recipient_id = ?", (recipient_id,))
    if len(rows) == 0:
        raise NotFoundError("Recipient " + recipient_id + " was not found.")
    return Recipient(*rows[0])


def get_recipients(search=""):
    recipients = []
    for row in get_rows("SELECT * FROM recipients ORDER BY recipient_id"):
        recipient = Recipient(*row)
        if search.lower() in (recipient.recipient_id + recipient.name + recipient.address).lower():
            recipients.append(recipient)
    return recipients


def check_recipient_data(data):
    """Check the values and return the cleaned name, contact and address."""
    name = check_text(data.name, "Name")
    contact = check_text(data.contact, "Contact")
    address = check_text(data.address, "Address")
    check_choice(data.recipient_type, RECIPIENT_TYPES, "Recipient type")
    return name, contact, address


def add_recipient(data):
    name, contact, address = check_recipient_data(data)
    new_id = make_id("REC", data.recipient_id, "recipients", "recipient_id")
    run("INSERT INTO recipients VALUES (?, ?, ?, ?, ?)", (new_id, name, contact, address, data.recipient_type))
    return new_id


def update_recipient(recipient_id, data):
    get_recipient(recipient_id)
    name, contact, address = check_recipient_data(data)
    run("UPDATE recipients SET name=?, contact=?, address=?, recipient_type=? WHERE recipient_id=?",
        (name, contact, address, data.recipient_type, recipient_id))


def delete_recipient(recipient_id):
    get_recipient(recipient_id)
    used = get_rows("SELECT COUNT(*) FROM distributions WHERE recipient_id = ?", (recipient_id,))[0][0]
    if used > 0:
        raise InvalidDataError("This recipient already has distributions. Delete them first.")
    run("DELETE FROM recipients WHERE recipient_id = ?", (recipient_id,))
