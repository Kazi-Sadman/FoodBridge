"""Recipient class: a person or group that receives food."""


class Recipient:
    def __init__(self, recipient_id, name, contact, address, recipient_type):
        self.recipient_id = recipient_id
        self.name = name
        self.contact = contact
        self.address = address
        self.recipient_type = recipient_type

    def to_dict(self):
        return {"recipient_id": self.recipient_id, "name": self.name, "contact": self.contact,
                "address": self.address, "recipient_type": self.recipient_type}
