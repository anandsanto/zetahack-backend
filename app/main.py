from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import CustomizeLogger
from app.core.config import settings
from app.core.crud import (
    add_transaction, delete_transaction,
    update_status, query_bill,
    add_customer, delete_customer,
    add_seller, delete_seller, query_cust, query_seller
)
import uuid
import json
from fastapi.exceptions import RequestValidationError, StarletteHTTPException, ValidationError
from fastapi import Request
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.middleware.middleware import (
    neccessary_middlware_ops,
)
from app.schemas.bills import (
    TransactionSchema, ActionResponseSchema, FilterBody
)

from app.schemas.general import (
    CustomerDetailsSchema, SellerDetailsSchema
)

def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        dependencies=[
            Depends(neccessary_middlware_ops)
        ]
    )
    _app.logger = CustomizeLogger.make_logger(False)



    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def request_exception_handler(request: Request, exc):
    exc_json = json.loads(exc.json())
    print(exc_json)

@app.post("/seller/api/addbill", response_model = ActionResponseSchema)
async def add_bill(*, billdata: TransactionSchema):

    billdata.bill_id = uuid.uuid4()
    ret = await add_transaction(billdata)
    return {'status': ret}

@app.post("/consumer/api/filterbills/{customer_id}")
async def filter_bill(*, customer_id : str, status: str, skip: int = 0, limit: int = 0, body: FilterBody):
    ret = await query_bill(customer_id, body, status, skip, limit)
    return {'data': ret}

@app.post("/consumer/api/getcustomer")
async def get_cust_details(*, customer_id: str, skip: int, limit: int,projection : dict):
    ret = await query_cust(customer_id, projection, skip, limit)
    return {'data': ret}

@app.post("/seller/api/getseller")
async def get_seller_details(seller_id : str, skip: int, limit: int, projection: dict):
    ret = await query_seller(seller_id, projection,skip, limit)
    return {'data': ret}

@app.put("/seller/api/updatebillstatus", response_model = ActionResponseSchema)
async def update_bill_status(*, bill_id: str, status: str):
    ret = await update_status(bill_id, status)
    if ret is None:
        return {'status': False}
    return {'status': ret["status"] == status}


@app.delete("/seller/api/deletebill", response_model = ActionResponseSchema)
async def delete_bill(*, bill_id: str):
    ret = await delete_transaction(bill_id)
    if ret is None:
        return {'status': False}
    return {'status': ret.deleted_count == 1}

@app.post("/general/api/addcust", response_model = ActionResponseSchema)
async def add_custtodb(*, custdata: CustomerDetailsSchema):

    custdata.customer_id = uuid.uuid4()
    ret = await add_customer(custdata)
    return {'status': ret}

@app.delete("/general/api/deletecust", response_model = ActionResponseSchema)
async def delete_custfromdb(*, cust_id: str):
    ret = await delete_customer(cust_id)
    if ret is None:
        return {'status': False}
    return {'status': ret.deleted_count == 1}

@app.post("/general/api/addseller", response_model = ActionResponseSchema)
async def add_sellertodb(*, sellerdata: SellerDetailsSchema):

    sellerdata.seller_id = uuid.uuid4()
    ret = await add_seller(sellerdata)
    return {'status': ret}

@app.delete("/general/api/deleteseller", response_model = ActionResponseSchema)
async def delete_sellerfromdb(*, seller_id: str):
    ret = await delete_seller(seller_id)
    if ret is None:
        return {'status': False}
    return {'status': ret.deleted_count == 1}


@app.on_event("startup")
async def startup_db():
    os.system("pip install pandas")
    try:
        await connect_to_mongo()
    except Exception as e:
        app.logger.critical(f"Not able to establish connection with MongoDB - {e}")


@app.on_event("shutdown")
async def shutdown_db():
    try:
        await close_mongo_connection()
    except Exception as e:
        app.logger.critical(f"Not able to gracefully close MongoDB connection - {e}")

