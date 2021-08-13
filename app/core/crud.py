#!/usr/bin/env python3
from ..schemas.bills import (
    TransactionSchema, FilterBody
)

from ..schemas.general import (
    CustomerDetailsSchema,
    SellerDetailsSchema
)
from . import mongodb
from pymongo import ReturnDocument
from datetime import datetime as dt
import json
import pandas as pd

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

async def add_customer(cust: CustomerDetailsSchema):
    coll = mongodb.db.client.zetabase.custcollection
    res = await coll.insert_one(cust.dict())
    return res.acknowledged

async def delete_customer(cust_id: str):
    coll = mongodb.db.client.zetabase.custcollection
    doc = await coll.delete_one(
        {'customer_id': cust_id},
    )
    return doc

async def add_seller(seller: SellerDetailsSchema):
    coll = mongodb.db.client.zetabase.sellercollection
    res = await coll.insert_one(seller.dict())
    return res.acknowledged

async def delete_seller(seller_id: str):
    coll = mongodb.db.client.zetabase.sellercollection
    doc = await coll.delete_one(
        {'seller_id': seller_id},
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

async def query_bill(customer_id: str, body : FilterBody, status: str, skip, limit):
    try:
        coll = mongodb.db.client.zetabase.billcollection
        ret_doc = []
        print("BODY", body)
        if status == 'pending':
            pipeline = [{'$match' : { 'customer_id' : customer_id }},{'$project': {'seller_id': 1, '_id': 0,'timestamp': 1, 'total': { '$sum': "$items.price"}}}]
            cursor = coll.aggregate(pipeline)#.skip(skip).limit(limit)

            async for document in cursor:
                document['timestamp'] = str(document['timestamp'])
                ret_doc.append(document)
        else:
            projection = {'items':1, 'seller_id':1, 'timestamp':1}
            body = body.dict()
            body1 = {}
            print(body)
            for key in body:
                if body[key] is not None:
                    if key in ['product_category', 'name'] :
                        print("KEY", key)
                        body1['items.'+key] = body[key]
            print({'customer_id': customer_id, **body1})
            cursor = coll.find({'customer_id': customer_id,'status': 'success', **body1}, projection).skip(skip).limit(limit)
            async for document in cursor:
                ret = {}
                #print(document)
                ret['seller_id'] = document['seller_id']
                ret['timestamp'] = document['timestamp']
                df = pd.DataFrame(document['items'])
                #print(df.head())
                query_df = f"name=='{body1.get('items.name', None)}'"
                query_df1 = f"product_category=='{body1.get('items.product_category',None)}'"
                if 'items.name' in body1 and 'items.product_category' in body1:

                    query_f = query_df + ' and '+query_df1
                    df = df.query(query_f)
                    #print("Hye", df)
                elif 'items.name' in body1:
                    query_f = query_df
                    df = df.query(query_f)
                elif 'items.product_category' in body1:
                    query_f = query_df1
                    df = df.query(query_f)
                else:
                    pass
                ret['items'] = df.reset_index(drop=True).to_dict('r')
                ret_doc.append(ret)
        return ret_doc
    except Exception as e:
        print("Exception", e)

async def query_cust(customer_id: str, projection: dict, skip: int, limit: int):
    coll = mongodb.db.client.zetabase.custcollection
    if customer_id is None:
        query = {}
    else:
        query = {'customer_id': customer_id}
    cursor = coll.find(query, projection).skip(skip).limit(limit)
    ret_doc = []
    async for document in cursor:
        ret_doc.append(document)
    return ret_doc

async def query_seller(seller_id, projection: dict, skip: int, limit: int):
    coll = mongodb.db.client.zetabase.sellercollection
    if seller_id is None:
        query = {}
    else:
        query = {'seller_id': seller_id}
    cursor = coll.find(query, projection).skip(skip).limit(limit)
    ret_doc = []
    async for document in cursor:
        ret_doc.append(document)
    return ret_doc