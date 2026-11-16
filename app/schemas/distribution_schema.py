from fastapi import APIRouter
from app.schemas.distribution_schema import DistributionCreate
from app.services import distribution_service

router = APIRouter(prefix="/distributions", tags=["Distributions"])


@router.get("")
def list_distributions():
    distributions = distribution_service.get_distributions()
    return [distribution.to_dict() for distribution in distributions]


@router.post("", status_code=201)
def add_distribution(data: DistributionCreate):
    new_id = distribution_service.add_distribution(data)
    return {"message": "Distribution " + new_id + " saved."}


@router.delete("/{distribution_id}")
def delete_distribution(distribution_id: str):
    distribution_service.delete_distribution(distribution_id)
    return {"message": "Distribution deleted."}
