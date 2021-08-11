#!/usr/bin/env python3
from ..schemas.bills import TransactionSchema
from . import mongodb
from pymongo import ReturnDocument
from datetime import datetime as dt
import json


async def add_transaction(tran: TransactionSchema):
    coll = mongodb.db.client.zetabase.billcollection
    res = await coll.insert_one(tran.dict())
    return res.acknowledged

async def delete_transaction(bill_id: str):
    coll = mongodb.db.client.zetabase.billcollection
    doc = await coll.delete_one(
        {'bill_id': bill_id},
    )
    return doc


async def update_status(bill_id: str, status: str):
    coll = mongodb.db.client.zetabase.billcollection
    doc = await coll.find_one_and_update(
        {'bill_id': bill_id},
        {'$set': {'status': status}},
        return_document=ReturnDocument.AFTER
    )
    return doc

async def query_bill(customer_id: str, skip, limit):
    coll = mongodb.db.client.zetabase.billcollection
    cursor = coll.find({'customer_id': {'$eq': customer_id}}).skip(skip).limit(limit)
    ret_doc = []
    async for document in cursor:
        document['_id'] = str(document['_id'])
        document['bill_id'] = str(document['bill_id'])
        document['timestamp'] = str(document['timestamp'])
        ret_doc.append(document)
    return ret_doc