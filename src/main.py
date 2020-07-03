from decimal import Decimal

import requests
from fastapi import FastAPI, Header, HTTPException, Response

import utils
from models import CalcRequest, CalcResponse

app = FastAPI()


@app.post("/calc/", response_model=CalcResponse)
def calc(
    request: CalcRequest, response: Response,
    sign:str = Header(None)
):
    if sign != utils.sign_dict(request.dict()):
        raise HTTPException(status_code=400, detail="Sign is not correct")
    try:
        rate = utils.get_rate(request.in_currency + request.out_currency)
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=400, detail="Currency destination is not supported")
    calc_response = CalcResponse(
        rate=rate, out_amount=str(Decimal(request.in_amount) * Decimal(rate)
    )
    response.headers["sign"] = utils.sign_dict(calc_response.dict())
    return calc_response
