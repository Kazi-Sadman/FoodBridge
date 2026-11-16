from fastapi import APIRouter
from app.schemas.donation_schema import DonationCreate, DonationUpdate
from app.services import donation_service

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.get("")
def list_donations(search: str = "", category: str = "All"):
    donations = donation_service.get_donations(search, category)
    return [donation.to_dict() for donation in donations]


@router.get("/{donation_id}")
def get_donation(donation_id: str):
    return donation_service.get_donation(donation_id).to_dict()


@router.post("", status_code=201)
def add_donation(data: DonationCreate):
    new_id = donation_service.add_donation(data)
    return {"message": "Donation " + new_id + " added."}


@router.put("/{donation_id}")
def update_donation(donation_id: str, data: DonationUpdate):
    donation_service.update_donation(donation_id, data)
    return {"message": "Donation updated."}


@router.delete("/{donation_id}")
def delete_donation(donation_id: str):
    donation_service.delete_donation(donation_id)
    return {"message": "Donation deleted."}
