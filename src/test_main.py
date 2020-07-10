import aiohttp
from fastapi.testclient import TestClient

from main import app
from utils import sign_dict

test_data = {
    "in_currency": "BTC",
    "out_currency": "USDT",
    "in_amount": "2",
}


class MockResponse:
    @staticmethod
    async def raise_for_status():
        pass

    @staticmethod
    async def json():
        return {"symbol": "BTCUSDT", "price": "9090.72000000"}


class MockSession:
    async def __aenter__(self):
        return MockResponse

    async def __aexit__(self, *args):
        pass


def test_calc(monkeypatch, event_loop):
    def mock_get(*args, **kwargs):
        return MockSession()

    client = TestClient(app)
    monkeypatch.setattr(aiohttp.ClientSession, "get", mock_get)
    assert client.post(
        "/calc/",
        json=test_data,
        headers={
            "Sign": "1a40d06367165e81feb61b07e07f21e70ae7b4d63fda3fa127194ec3bdfae87bce14948fc2ac60d3f2fe8f47e01bf9df71518299aae6f9abaa05181e8de25fa3"
        },
    ).json() == {"out_amount": "18181.44000000", "rate": "9090.72000000",}
