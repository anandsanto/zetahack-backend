#!/usr/bin/env python3
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime


class CustomerDetailsSchema(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    age: int
    phone: str
    address: str
    member_since: datetime

    @validator('phone')
    def mobile_num_be_ten_digits(cls, v):
        if v.startswith('+91'):
            if not v[1:].isnumeric():
                raise ValueError('Mobile phone numbers must be numeric')
            elif len(v) != 13:
                raise ValueError('Mobile phone numbers must be 10 digits long')
            else:
                return v

        elif len(v) != 10:
            raise ValueError('Mobile phone numbers must be 10 digits long')

        elif not v.isnumeric():
            raise ValueError('Mobile phone numbers must be numeric')

        return '+91' + v

    class Config:
        orm_mode = True


class SellerDetailsSchema(BaseModel):
    seller_id: str
    store_name: str
    contact_person_first_name: str
    contact_person_last_name: str
    phone: str
    store_address: str
    member_since: datetime

    @validator('phone')
    def mobile_num_be_ten_digits(cls, v):
        if v.startswith('+91'):
            if not v[1:].isnumeric():
                raise ValueError('Mobile phone numbers must be numeric')
            elif len(v) != 13:
                raise ValueError('Mobile phone numbers must be 10 digits long')
            else:
                return v

        elif len(v) != 10:
            raise ValueError('Mobile phone numbers must be 10 digits long')

        elif not v.isnumeric():
            raise ValueError('Mobile phone numbers must be numeric')

        return '+91' + v

    class Config:
        orm_mode = True
