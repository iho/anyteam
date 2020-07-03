from utils import get_rate, sign_dict

import requests_mock

test_data = {
    "in_currency": "BTC",
    "out_currency": "USDT",
    "in_amount": "2",
}


def test_sign_dict():
    assert (
        sign_dict(test_data)
        == "5d66116fbc095519e395bd94ff77f17ca4b01b69d6c6ff1e46bc2ce1a5494f87646bc91392ac27874f417ef2594d91e05232d7affddeb836d21971228595c5f7"
    )


def test_get_rate():
    with requests_mock.Mocker() as m:
        m.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", json={"symbol": "BTCUSDT", "price": "9090.72000000"})
        assert get_rate("BTCUSDT") == "9090.72000000"
