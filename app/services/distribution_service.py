"""Distribution logic. Main rule: never give away more food than is left in a donation."""

from datetime import date
from app.exceptions import InvalidDataError, NotFoundError
from app.models.database import run, get_rows
from app.models.distribution import Distribution
from app.services import donation_service, recipient_service
from app.services.validation import check_quantity, make_id


def get_distributions():
    rows = get_rows("""SELECT x.distribution_id, x.donation_id, d.food_name, x.recipient_id, r.name,
                       x.quantity, d.unit, x.distribution_date
                       FROM distributions x
                       JOIN donations d ON d.donation_id = x.donation_id
                       JOIN recipients r ON r.recipient_id = x.recipient_id
                       ORDER BY x.distribution_id""")
    distributions = []
    for row in rows:
        distributions.append(Distribution(*row))
    return distributions


def add_distribution(data):
    donation = donation_service.get_donation(data.donation_id)
    recipient_service.get_recipient(data.recipient_id)
    check_quantity(data.quantity)
    if donation.is_expired():
        raise InvalidDataError("This donation has expired and cannot be distributed.")
    if data.distribution_date > date.today():
        raise InvalidDataError("Distribution date cannot be in the future.")
    if data.quantity > donation.remaining():
        raise InvalidDataError("Only " + str(donation.remaining()) + " " + donation.unit
                               + " is left, but you asked for " + str(data.quantity) + ".")
    new_id = make_id("DIS", data.distribution_id, "distributions", "distribution_id")
    run("INSERT INTO distributions VALUES (?, ?, ?, ?, ?)",
        (new_id, data.donation_id, data.recipient_id, data.quantity, str(data.distribution_date)))
    return new_id


def delete_distribution(distribution_id):
    rows = get_rows("SELECT * FROM distributions WHERE distribution_id = ?", (distribution_id,))
    if len(rows) == 0:
        raise NotFoundError("Distribution " + distribution_id + " was not found.")
    run("DELETE FROM distributions WHERE distribution_id = ?", (distribution_id,))
