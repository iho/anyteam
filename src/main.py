import asyncio
import os
from decimal import Decimal

import aiohttp
from fastapi import FastAPI, Header, HTTPException, Response

import utils
from models import CalcRequest, CalcResponse

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    currencies = os.environ["PRECACHED_CURRENCY_DESTINATIONS"].split(",")
    await asyncio.gather(*[utils.cache.get_rate(currency) for currency in currencies])


@app.on_event("shutdown")
async def shutdown_event():
    if utils.cache.session is not None:
        await utils.cache.session.close()


@app.post("/calc/", response_model=CalcResponse)
async def calc(request: CalcRequest, response: Response, sign: str = Header(None)):
    if sign != utils.sign_dict(request.dict()):
        raise HTTPException(status_code=400, detail="Sign is not correct")
    try:
        rate = await utils.cache.get_rate(request.in_currency + request.out_currency)
    except (
        aiohttp.client_exceptions.ClientResponseError,
        asyncio.exceptions.TimeoutError,
    ):
        raise HTTPException(
            status_code=400, detail="Currency destination is not supported"
        )
    calc_response = CalcResponse(
        rate=rate, out_amount=str(Decimal(request.in_amount) * Decimal(rate))
    )
    response.headers["sign"] = utils.sign_dict(calc_response.dict())
    return calc_response
