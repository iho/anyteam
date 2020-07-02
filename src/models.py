from pydantic import BaseModel


class CalcRequest(BaseModel):
    in_currency: str
    out_currency: str
    in_amount: str


class CalcResponse(BaseModel):
    rate: str
    out_amount: str
