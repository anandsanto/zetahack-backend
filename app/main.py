from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging import CustomizeLogger
from app.core.config import settings
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.middleware.middleware import (
    neccessary_middlware_ops,
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
