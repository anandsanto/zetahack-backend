from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import CustomizeLogger
from app.core.config import settings
from app.core.crud import (
    add_transaction, delete_transaction,
    update_status
)
import uuid
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.middleware.middleware import (
    neccessary_middlware_ops,
)
from app.schemas.bills import TransactionSchema, ActionResponseSchema

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


@app.post("/seller/api/addbill", response_model = ActionResponseSchema)
async def add_bill(*, billdata: TransactionSchema):

    billdata.bill_id = uuid.uuid4()
    ret = await add_transaction(billdata)
    return {'status': ret}


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



@app.on_event("startup")
async def startup_db():
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
