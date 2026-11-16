from fastapi import APIRouter
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def summary():
    return report_service.get_summary()


@router.get("/totals")
def totals_by_unit():
    return report_service.get_totals_by_unit()


@router.get("/categories")
def category_counts():
    return report_service.get_category_counts()


@router.get("/donors")
def donors():
    return report_service.get_donors()


@router.get("/expired")
def expired_donations():
    return [donation.to_dict() for donation in report_service.get_expired_donations()]


@router.get("/recipients")
def recipient_summary():
    return report_service.get_recipient_summary()
