import asyncio
import hashlib
import hmac
import os
from decimal import *
from typing import Dict, Optional

import aiohttp
import requests
from aiocache import Cache, cached

API_KEY = "Test_Keys_12345"
API_URL = "https://api.binance.com/"

getcontext().prec = 18


def sign_dict(dict_) -> str:
    string = "".join(map(lambda x: x[1], sorted(dict_.items(), key=lambda x: x[0])))
    return hmac.new(
        API_KEY.encode("utf-8"), string.encode("utf-8"), hashlib.sha512
    ).hexdigest()


class BinanceCache:
    session: Optional[aiohttp.ClientSession] = None
    locks: Dict[str, asyncio.Lock] = {}

    async def get_rate(self, symbol) -> str:
        lock = self.locks.get(symbol)
        if not lock:
            lock = self.locks[symbol] = asyncio.Lock()
        await lock.acquire()
        try:
            return await asyncio.wait_for(self._get_rate(symbol), timeout=5.0)
        finally:
            lock.release()

    @cached(cache=Cache.MEMORY, ttl=600)
    async def _get_rate(self, symbol) -> str:
        if not self.session:
            loop = asyncio.get_event_loop()
            self.session = aiohttp.ClientSession(loop=loop)
        url = API_URL + f"api/v3/ticker/price?symbol={symbol}"
        async with self.session.get(url) as response:
            response.raise_for_status()
            resp = await response.json()
            return resp["price"]


cache = BinanceCache()
