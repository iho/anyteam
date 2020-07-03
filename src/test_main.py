import requests
from fastapi.testclient import TestClient

from main import app
from utils import sign_dict

client = TestClient(app)

test_data = {
    "in_currency": "BTC",
    "out_currency": "USDT",
    "in_amount": "2",
}


class MockResponse:
    @staticmethod
    def raise_for_status():
        pass

    @staticmethod
    def json():
        return {"symbol": "BTCUSDT", "price": "9090.72000000"}


def test_calc(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    assert client.post("/calc/", json=test_data).json() == {
        "out_amount": "18181.44000000",
        "rate": "9090.72000000",
    }
