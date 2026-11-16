"""Donation logic: get, search, add, update, delete."""

from app.exceptions import InvalidDataError, NotFoundError
from app.models.choices import FOOD_CATEGORIES, FOOD_UNITS
from app.models.database import run, get_rows
from app.models.donation import Donation
from app.services.validation import check_text, check_choice, check_quantity, make_id

# Gets every donation and adds the total distributed quantity as the last column.
DONATION_SQL = """SELECT d.*, COALESCE((SELECT SUM(quantity) FROM distributions
                  WHERE donation_id = d.donation_id), 0) FROM donations d"""


def get_donation(donation_id):
    rows = get_rows(DONATION_SQL + " WHERE d.donation_id = ?", (donation_id,))
    if len(rows) == 0:
        raise NotFoundError("Donation " + donation_id + " was not found.")
    return Donation(*rows[0])


def get_donations(search="", category="All"):
    donations = []
    for row in get_rows(DONATION_SQL + " ORDER BY d.donation_id"):
        donation = Donation(*row)
        text = (donation.donation_id + donation.donor_name + donation.food_name).lower()
        if search.lower() in text and (category == "All" or donation.category == category):
            donations.append(donation)
    return donations


def check_donation_data(data):
    """Check the values of a new or updated donation and return the cleaned donor and food names."""
    donor = check_text(data.donor_name, "Donor name")
    food = check_text(data.food_name, "Food name")
    check_choice(data.category, FOOD_CATEGORIES, "Category")
    check_choice(data.unit, FOOD_UNITS, "Unit")
    check_quantity(data.quantity)
    return donor, food


def add_donation(data):
    donor, food = check_donation_data(data)
    new_id = make_id("DON", data.donation_id, "donations", "donation_id")
    run("INSERT INTO donations VALUES (?, ?, ?, ?, ?, ?, ?)",
        (new_id, donor, food, data.category, data.quantity, data.unit, str(data.expiry_date)))
    return new_id


def update_donation(donation_id, data):
    donation = get_donation(donation_id)
    donor, food = check_donation_data(data)
    if data.quantity < donation.distributed:
        raise InvalidDataError("Quantity cannot be less than the " + str(donation.distributed) + " already distributed.")
    run("UPDATE donations SET donor_name=?, food_name=?, category=?, quantity=?, unit=?, expiry_date=? WHERE donation_id=?",
        (donor, food, data.category, data.quantity, data.unit, str(data.expiry_date), donation_id))


def delete_donation(donation_id):
    donation = get_donation(donation_id)
    if donation.distributed > 0:
        raise InvalidDataError("This donation already has distributions. Delete them first.")
    run("DELETE FROM donations WHERE donation_id = ?", (donation_id,))
