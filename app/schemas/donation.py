
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationtBase(BaseModel):
    id: int
    comment: Optional[str] = Field(..., min_length=1)
    full_amount: PositiveInt
    create_date: datetime

    class Config:
        orm_mode = True


class DonationGet(DonationtBase):
    invested_amount: int
    fully_invested: bool
    close_date: datetime = None
    user_id: int


class DonationPost(BaseModel):
    comment: Optional[str] = Field(None, min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        orm_mode = True


class DonationPostReturn(DonationPost):
    create_date: datetime
    id: int
