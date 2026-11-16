"""Distribution class: food from one donation given to one recipient."""


class Distribution:
    def __init__(self, distribution_id, donation_id, food_name, recipient_id, recipient_name, quantity, unit, distribution_date):
        self.distribution_id = distribution_id
        self.donation_id = donation_id
        self.food_name = food_name
        self.recipient_id = recipient_id
        self.recipient_name = recipient_name
        self.quantity = quantity
        self.unit = unit
        self.distribution_date = distribution_date

    def to_dict(self):
        return {"distribution_id": self.distribution_id, "donation_id": self.donation_id, "food_name": self.food_name,
                "recipient_id": self.recipient_id, "recipient_name": self.recipient_name,
                "quantity": self.quantity, "unit": self.unit, "distribution_date": self.distribution_date}
