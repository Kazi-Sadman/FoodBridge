"""Reports and analysis. Units (kg, liter ...) are never added together."""

from app.models.choices import FOOD_CATEGORIES
from app.models.database import get_rows
from app.services import donation_service, distribution_service, recipient_service


def get_summary():
    """Main numbers for the dashboard."""
    donations = donation_service.get_donations()
    available = 0
    expired = 0
    for donation in donations:
        if donation.status() == "Available":
            available += 1
        if donation.is_expired():
            expired += 1
    return {"donations": len(donations), "available": available, "expired": expired,
            "recipients": len(recipient_service.get_recipients()),
            "distributions": len(distribution_service.get_distributions()),
            "donors": len(get_donors())}


def get_totals_by_unit():
    """List of rows: unit, donated, distributed, remaining."""
    totals = {}  # dictionary: unit -> numbers
    for donation in donation_service.get_donations():
        if donation.unit not in totals:
            totals[donation.unit] = {"unit": donation.unit, "donated": 0, "distributed": 0, "remaining": 0}
        totals[donation.unit]["donated"] += donation.quantity
        totals[donation.unit]["distributed"] += donation.distributed
        totals[donation.unit]["remaining"] += donation.remaining()
    return list(totals.values())


def get_category_counts():
    """Dictionary: category -> number of donations."""
    counts = {}
    for category in FOOD_CATEGORIES:
        counts[category] = 0
    for donation in donation_service.get_donations():
        counts[donation.category] += 1
    return counts


def get_donors():
    """A set keeps every donor name only once. We return it as a sorted list."""
    donors = set()
    for donation in donation_service.get_donations():
        donors.add(donation.donor_name)
    return sorted(donors)


def get_expired_donations():
    expired = []
    for donation in donation_service.get_donations():
        if donation.is_expired():
            expired.append(donation)
    return expired


def get_recipient_summary():
    """For each recipient: number of distributions and total quantity (SQL GROUP BY)."""
    rows = get_rows("""SELECT r.name, COUNT(x.distribution_id), COALESCE(SUM(x.quantity), 0)
                       FROM recipients r LEFT JOIN distributions x ON x.recipient_id = r.recipient_id
                       GROUP BY r.recipient_id ORDER BY r.recipient_id""")
    summary = []
    for name, count, total in rows:
        summary.append({"recipient": name, "distributions": count, "total_quantity": total})
    return summary
