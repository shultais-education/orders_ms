from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional


class RUPhoneNumber(PhoneNumber):
    default_region_code = 'RU'
    supported_regions = ['RU']
    phone_format = 'E164' # 'NATIONAL'


class OrderDetail(BaseModel):
    id: int
    house_id: int

    user_name: str = Field(min_length=1, max_length=100)
    user_email: EmailStr
    user_phone: str


class OrderRequest(BaseModel):
    house_id: int

class Order(BaseModel):
    house_id: int

    user_name: str = Field(min_length=1, max_length=100)
    user_email: EmailStr
    user_phone: Optional[RUPhoneNumber] = Field(default="")
