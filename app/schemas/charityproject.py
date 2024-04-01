from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator, Extra

from app.schemas.constants import CREATE_TIME, CLOSE_TIME


class BaseCharityProject(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, example='Example')
    description: Optional[str] = Field(min_length=1)
    full_amount: Optional[int] = Field(gt=0, example=1000)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(BaseCharityProject):
    name: str = Field(min_length=1, max_length=100, example='Example')
    description: str = Field(min_length=1)
    full_amount: int = Field(gt=0, example=1000)


class CharityProjectDB(BaseCharityProject):
    id: int
    invested_amount: int = Field(example=500)
    fully_invested: bool
    create_date: datetime = Field(example=CREATE_TIME)
    close_date: Optional[datetime] = Field(example=CLOSE_TIME)

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseCharityProject):
    ...

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')

        return value
