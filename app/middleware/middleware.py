from fastapi import Request, Header
from app.core.logging import LoggerDetails
import uuid


async def neccessary_middlware_ops(request: Request):
    request.state.id = uuid.uuid4()
