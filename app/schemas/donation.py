from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra

from app.schemas.constants import CREATE_TIME, CLOSE_TIME


class BaseDonation(BaseModel):
    full_amount: int = Field(gt=0, example=1000)
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(BaseDonation):
    ...


class DonationDB(BaseDonation):
    id: int
    create_date: datetime = Field(example=CREATE_TIME)
    user_id: int
    invested_amount: int = Field(example=500)
    fully_invested: bool
    close_date: datetime = Field(None, example=CLOSE_TIME)

    class Config:
        orm_mode = True


class DonationByUser(BaseDonation):
    id: int
    full_amount: int = Field(gt=-1, example=1000)
    create_date: datetime = Field(example=CREATE_TIME)

    class Config:
        orm_mode = True
