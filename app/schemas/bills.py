#!/usr/bin/env python3
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from datetime import datetime

class ItemSchema(BaseModel):
    name: str
    price: float
    quantity: float
    quantity_type: int # 0 - weight(kg), volume (l), quantized (3)
    product_category: Optional[str] = None


class TransactionSchema(BaseModel):
    bill_id: str = ''
    timestamp: datetime
    seller_id: str
    customer_id: str
    items: List[ItemSchema]

class ActionResponseSchema(BaseModel):
    status: bool
    reason_failed: str = None
