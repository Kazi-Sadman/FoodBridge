"""Talks to the FastAPI backend. Pages never touch the database directly."""

import requests

BASE_URL = "http://127.0.0.1:8000"


def call_api(method, path, data=None, params=None):
    """Send one request. Problems are raised as ValueError so pages can show them."""
    try:
        response = requests.request(method, BASE_URL + path, json=data, params=params, timeout=5)
    except requests.exceptions.RequestException:
        raise ValueError("Cannot reach the backend. Start it with: uvicorn app.main:app --reload")

    if response.status_code >= 400:
        detail = response.json().get("detail", "Something went wrong.")
        if isinstance(detail, list):  # a pydantic error (wrong type or missing field)
            detail = "Please check the form values: " + str(detail[0]["msg"])
        raise ValueError(str(detail))
    return response.json()


def get(path, params=None):
    return call_api("GET", path, params=params)


def post(path, data):
    return call_api("POST", path, data=data)


def put(path, data):
    return call_api("PUT", path, data=data)


def delete(path):
    return call_api("DELETE", path)
