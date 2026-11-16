from fastapi import APIRouter
from app.schemas.recipient_schema import RecipientCreate, RecipientUpdate
from app.services import recipient_service

router = APIRouter(prefix="/recipients", tags=["Recipients"])


@router.get("")
def list_recipients(search: str = ""):
    recipients = recipient_service.get_recipients(search)
    return [recipient.to_dict() for recipient in recipients]


@router.get("/{recipient_id}")
def get_recipient(recipient_id: str):
    return recipient_service.get_recipient(recipient_id).to_dict()


@router.post("", status_code=201)
def add_recipient(data: RecipientCreate):
    new_id = recipient_service.add_recipient(data)
    return {"message": "Recipient " + new_id + " added."}


@router.put("/{recipient_id}")
def update_recipient(recipient_id: str, data: RecipientUpdate):
    recipient_service.update_recipient(recipient_id, data)
    return {"message": "Recipient updated."}


@router.delete("/{recipient_id}")
def delete_recipient(recipient_id: str):
    recipient_service.delete_recipient(recipient_id)
    return {"message": "Recipient deleted."}
