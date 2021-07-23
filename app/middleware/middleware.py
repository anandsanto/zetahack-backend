from fastapi import Request, Header
from app.core.logging import LoggerDetails
import uuid


async def neccessary_middlware_ops(request: Request):
    request.state.id = uuid.uuid4()
    request.state.logger = request.state.logger.bind(request_details = await LoggerDetails.request_details_extract(request))
