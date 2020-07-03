import hashlib
import hmac
import os
from decimal import *

import requests
from cachetools import TTLCache, cached

API_KEY = os.environ["API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
API_URL = "https://api.binance.com/"

getcontext().prec = 18


def sign_dict(dict_) -> str:
    string = "".join(map(lambda x: x[1], sorted(dict_.items(), key=lambda x: x[0])))
    return hmac.new(
        API_KEY.encode("utf-8"), string.encode("utf-8"), hashlib.sha512
    ).hexdigest()


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_rate(symbol) -> str:
    url = API_URL + f"api/v3/ticker/price?symbol={symbol}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["price"]
