from decimal import Decimal
from typing import Optional

from fastapi import FastAPI, Response

import utils
from models import CalcRequest, CalcResponse

app = FastAPI()


@app.post("/calc/", response_model=CalcResponse)
async def calc(
    request: CalcRequest, response: Response,
):
    rate = utils.get_rate(request.in_currency + request.out_currency)
    calc_response = CalcResponse(
        rate=rate, out_amount=str(Decimal(request.in_amount) * Decimal(rate))
    )
    # import ipdb;ipdb.set_trace()
    response.headers["sign"] = utils.sign_dict(calc_response.dict())
    return calc_response