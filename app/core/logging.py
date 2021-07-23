import os
import logging
import sys

#from gunicorn.app.base import BaseApplication
from loguru import logger
from app.core.config import settings
from app.core.index import app_constants

base_level = settings.LOGGER_LEVEL


class InterceptHandler(logging.Handler):
    def emit(self, record):
        level = ""
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        log = logger.bind(request_details='zeta-app')

        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

if settings.PRODUCTION is True:

    from gunicorn.glogging import Logger
    class StubbedGunicornLogger(Logger):
        def setup(self, cfg):
            handler = logging.NullHandler()
            self.error_logger = logging.getLogger("gunicorn.error")
            self.error_logger.addHandler(handler)
            self.access_logger = logging.getLogger("gunicorn.access")
            self.access_logger.addHandler(handler)
            self.error_logger.setLevel(base_level)
            self.access_logger.setLevel(base_level)


class CustomizeLogger:

    log_format = ("<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}"+
        "</green> request details: {extra[request_details]} -"+
        " <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")

    @classmethod
    def filter_info(cls, record):
        return record["level"].name == 'INFO'

    @classmethod
    def filter_error(cls, record):
        return record["level"].name == 'ERROR'

    @classmethod
    def filter_debug(cls, record):
        return record["level"].name == 'DEBUG'

    @classmethod
    def filter_warning(cls, record):
        return record["level"].name == 'WARNING'

    @classmethod
    def filter_critical(cls, record):
        return record["level"].name == 'CRITICAL'


    @classmethod
    def make_logger(cls, is_stdaln: bool):
        logger_ret = logger.bind(request_details='zeta-app') if is_stdaln else cls.customize_logging()

        if is_stdaln:
            logger_ret.remove()

        for sink, func in zip([app_constants['file_info'],app_constants['file_error'],app_constants['file_debug'],app_constants['file_warning'],app_constants['file_critical']],[cls.filter_info, cls.filter_error, cls.filter_debug, cls.filter_warning, cls.filter_critical]):
            logger_ret.add(sink, level = base_level, filter = func, enqueue = True, format = cls.log_format)

        return logger_ret

    @classmethod
    def customize_logging(cls):
        logger.remove()
        seen = set()
        intercepting_list = [*logging.root.manager.loggerDict.keys(),"fastapi","uvicorn","uvicorn.access","uvicorn.error"]

        if settings.PRODUCTION is True:
            intercepting_list.extend(["gunicorn", "gunicorn.access", "gunicorn.error"])

        for name in intercepting_list:
            if name not in seen:
                seen.add(name.split(".")[0])
                logging.getLogger(name).handlers = [InterceptHandler()]
        return logger.bind(request_details = 'zeta-app')

class LoggerDetails:

    @staticmethod
    async def request_details_extract(request):
        headers_to_remove = []
        data_fields_to_remove = []

        op_id = str(request.state.id)
        headers= None if request.headers is None else dict(request.headers.items())

        for header in headers_to_remove:
            headers.pop(header, None)

        method = request.method
        query_params = None if request.query_params is None else dict(request.query_params.items())
        path_params = None if request.path_params is None else dict(request.path_params.items())

        cookies = None if request.cookies is None else dict(request.cookies.items())
        client = None if request.client is None else request.client._asdict()
        path = request.url.path
        data = {} if method!='POST' else await request.json()

        for field in data_fields_to_remove:
            if field == 'user' and field in data.keys():
                data['user'].pop('password',None)
            else:
                data.pop(field, None)

        return {
            'op_id': op_id,
            'headers': header,
            'method': method,
            'query_params' : query_params,
            'path_params': path_params,
            'cookies': cookies,
            'client': client,
            'path': path,
            'data': data,
        }
