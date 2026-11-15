# FoodBridge – Community Food Donation Coordinator

Records food donations, recipients and distributions, and shows how much food is left.
**Backend:** FastAPI + SQLite. **Frontend:** Streamlit. Data is saved in `app/data/foodbridge.db`
(created automatically with 12 donations, 5 recipients and 5 distributions the first time).

**Problem:** extra food is wasted or given twice. **Users:** volunteers and coordinators.
**Objectives:** record data, never give away more than what is left, block expired food, show summaries.

## Run (two terminals, both in the project folder)

```
pip install -r requirements.txt
uvicorn app.main:app --reload              # terminal 1: backend  (docs: http://127.0.0.1:8000/docs)
streamlit run frontend/streamlit_app.py    # terminal 2: frontend (http://localhost:8501)
```

## File structure

```
app/                        BACKEND
  main.py                   starts FastAPI, connects the routes, handles errors
  exceptions.py             custom errors with status codes
  models/                   classes + SQLite
    database.py             SQLite: connect, tables, sample data
    choices.py              tuples (categories, units, recipient types)
    donation.py  recipient.py  distribution.py     one class per file
  schemas/                  Pydantic: checks the shape of incoming data
    donation_schema.py  recipient_schema.py  distribution_schema.py
  services/                 business logic and validation
    validation.py  donation_service.py  recipient_service.py
    distribution_service.py  report_service.py
  routes/                   API URLs (thin: call a service, return the result)
    donation_routes.py  recipient_routes.py  distribution_routes.py  report_routes.py
frontend/                   FRONTEND
  streamlit_app.py          menu and page selection
  api_client.py             sends requests to the backend
  ui_helpers.py             choices and table helper
  views/                    dashboard_page.py donation_page.py recipient_page.py
                            distribution_page.py report_page.py
```

## Requirement checklist

| Requirement                | Where                                                                           |
| -------------------------- | ------------------------------------------------------------------------------- |
| GUI / menu (FR-1)          | `frontend/` sidebar menu, tabs, forms                                           |
| 5+ operations (FR-2)       | add, view, search, filter, update, delete, give food, reports                   |
| Persistent data (FR-3)     | SQLite file, `app/models/database.py`                                           |
| Validation (FR-4)          | `app/services/validation.py`, schemas, service rules                            |
| Analysis (FR-5)            | `app/services/report_service.py` (totals, categories, SQL GROUP BY)             |
| Functions + classes (FR-6) | services (functions), `app/models/` (classes)                                   |
| Error recovery (FR-7)      | custom errors → clear messages; frontend shows them and keeps running           |
| list / tuple / set / dict  | lists of objects; tuples in `choices.py`; set of IDs and donors; dict of totals |
| Library use                | `sqlite3`, `datetime`, `fastapi`, `pydantic`, `streamlit`, `requests`           |
