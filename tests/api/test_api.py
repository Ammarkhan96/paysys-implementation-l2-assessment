import pytest
import requests
import os

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080/api")

def test_api_health():
    res = requests.get(f"{BASE_URL}/health", timeout=3)
    assert res.status_code == 200

def test_invalid_transaction_search():
    res = requests.get(f"{BASE_URL}/transactions/INVALID_REF_999", timeout=3)
    assert res.status_code == 404

def test_payment_creation_validation():
    payload = {"amount": -50}
    res = requests.post(f"{BASE_URL}/payments", json=payload, timeout=3)
    assert res.status_code == 400
