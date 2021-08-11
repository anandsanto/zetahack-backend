import aiohttp
import asyncio
import json
import random
from bson import json_util

from random import randrange
from datetime import datetime

from datetime import timedelta

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

    class Config:
        orm_mode = True


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

random.seed(10)

url = "http://127.0.0.1:8000/seller/api/addbill"
store_id = [1,2,3,4,5]
customer_id = [1,2,3,4,5,6,7,8,9,10]
quantity_type = [0,1,3]
quantized_name = ['AA - Batteries','Sensodyne - 100gm', 'Colgate Brush', 'Lays - med', 'Gems - small', 'Keychain', 'Bottle', 'Soap', 'Shampoo']
qauntity_name = ['Rice - loose', 'Sugar - loose', 'Flour - loose', 'Apple', 'Mango', 'Potato']
volumetric_name = ['Oil - loose', 'Milk - loose']
category = {
    'AA - Batteries': 'Utility',
    'Soap': 'Essential',
    'Shampoo': 'Essential',
    'Keychain': 'Utility',
    'Bottle': 'Utiltiy',
    'Sensodyne - 100gm': 'Essential',
    'Colgate Brush': 'Essential',
    'Lays - med': 'Food',
    'Gems - small': 'Food',
}
async def update_bill_data(session):
    random_to_choose_quantized = random.randint(1, len(quantized_name))
    random_to_choose_quantity = random.randint(1, len(qauntity_name))
    random_to_choose_volumetric = random.randint(1, len(volumetric_name))

    items = []
    post = {}
    random_item = random.randint(0, len(quantized_name) - 1)
    for _ in range(random_to_choose_quantized):
        item = {}
        item['name'] = quantized_name[random_item]
        item['price'] = random.randint(100, 500)
        item['quantity'] = random.randint(1,10)
        item['quantity_type'] = 2
        item['product_category'] = category.get(item['name'], 'Food')
        random_item+=1
        random_item = random_item%len(quantized_name)

        items.append(item)
    random_item = random.randint(0, len(qauntity_name) - 1)
    for _ in range(random_to_choose_quantity):
        item = {}
        item['name'] = qauntity_name[random_item]
        item['price'] = random.randint(100, 500)
        item['quantity'] = random.randint(1, 10)
        item['quantity_type'] = 0
        item['product_category'] = category.get(item['name'], 'Food')
        random_item+=1
        random_item = random_item % len(qauntity_name)
        items.append(item)
    random_item = random.randint(0, len(volumetric_name) - 1)
    for _ in range(random_to_choose_volumetric):
        item = {}

        item['name'] = volumetric_name[random_item]
        item['price'] = random.randint(100, 500)
        item['quantity'] = random.randint(1, 10)
        item['quantity_type'] = 1
        item['product_category'] = category.get(item['name'], 'Food')
        random_item += 1
        random_item = random_item % len(volumetric_name)
        items.append(item)

    post["customer_id"] = str(customer_id[random.randint(0,len(customer_id)-1)])
    post["seller_id"] = str(store_id[random.randint(0,len(store_id)-1)])
    d1 = datetime.strptime('8/11/2021 1:30 AM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('12/21/2021 11:00 PM', '%m/%d/%Y %I:%M %p')
    post["timestamp"] = str(random_date(d1, d2))
    post['bill_id'] = ''
    post['items'] = items
    async with session.post(url, json=post) as resp:
        data = await resp.json(content_type='application/json')
        stat = resp.status
        print("STAT", stat, "DATA", data)

async def gather():
    fns = []
    async with aiohttp.ClientSession() as session:
        for _ in range(1, 50):
            print("Done")
            fns.append(await update_bill_data(session))
        await asyncio.gather(*fns)

asyncio.run(gather())