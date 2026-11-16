"""Donation class: one food donation. 'distributed' is how much was already given away."""

from datetime import date


class Donation:
    def __init__(self, donation_id, donor_name, food_name, category, quantity, unit, expiry_date, distributed=0):
        self.donation_id = donation_id
        self.donor_name = donor_name
        self.food_name = food_name
        self.category = category
        self.quantity = quantity
        self.unit = unit
        self.expiry_date = expiry_date  # text like 2026-11-20
        self.distributed = distributed

    def remaining(self):
        return self.quantity - self.distributed

    def is_expired(self):
        return self.expiry_date < str(date.today())

    def status(self):
        if self.is_expired():
            return "Expired"
        if self.remaining() <= 0:
            return "Fully distributed"
        return "Available"

    def to_dict(self):
        return {"donation_id": self.donation_id, "donor_name": self.donor_name, "food_name": self.food_name,
                "category": self.category, "quantity": self.quantity, "unit": self.unit,
                "expiry_date": self.expiry_date, "remaining": self.remaining(), "status": self.status()}
