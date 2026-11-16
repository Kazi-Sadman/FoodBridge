"""FoodBridge backend (FastAPI). Run from the project folder with:  uvicorn app.main:app --reload
API documentation page: http://127.0.0.1:8000/docs"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.exceptions import FoodBridgeError
from app.models.database import setup_database
from app.routes import distribution_routes, donation_routes, recipient_routes, report_routes

setup_database()  # creates the SQLite file and sample data the first time

app = FastAPI(title="FoodBridge", description="Community Food Donation Coordinator")
app.include_router(donation_routes.router)
app.include_router(recipient_routes.router)
app.include_router(distribution_routes.router)
app.include_router(report_routes.router)


@app.exception_handler(FoodBridgeError)
def handle_error(request, error):
    """Turn any FoodBridge error into a JSON message with the right status code."""
    return JSONResponse(status_code=error.status_code, content={"detail": str(error)})


@app.get("/")
def home():
    return {"application": "FoodBridge", "docs_url": "/docs"}
