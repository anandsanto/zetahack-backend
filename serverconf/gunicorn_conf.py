#!/usr/bin/env python3

import json
import multiprocessing
import os
from app.core.config import settings
from app.core.logging import StubbedGunicornLogger

host = settings.HOST
port = settings.PORT
bind_env = os.getenv("BIND", None)
use_loglevel = settings.LOGGER_LEVEL.lower()
use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = float(settings.WORKERS_PER_CORE)
default_web_concurrency = workers_per_core * cores
web_concurrency = max(int(default_web_concurrency), 2)
accesslog_var = str(settings.ACCESSLOG)
use_accesslog = accesslog_var or None
errorlog_var = '-'
use_errorlog = errorlog_var or None

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
bind = use_bind
errorlog = use_errorlog
worker_tmp_dir = "/dev/shm"
accesslog = use_accesslog
graceful_timeout = settings.GRACEFULTIMEOUT
timeout = settings.TIMEOUT
keepalive = settings.KEEPALIVE


# For debugging and testing
options = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": None,
    "accesslog": accesslog,
    'worker_class': 'uvicorn.workers.UvicornWorker',
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    'logger_class': StubbedGunicornLogger,
    "host": host,
    "port": port,
}
