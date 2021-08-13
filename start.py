#!/usr/bin/env python3

from app.core.config import settings
from app.main import app
import uvicorn

if settings.PRODUCTION:

    from gunicorn.app.base import BaseApplication
    from serverconf import gunicorn_conf
    class StandaloneApplication(BaseApplication):
        """Our Gunicorn application."""

        def __init__(self, app, options):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {
                key: value for key, value in self.options.items()
                if key in self.cfg.settings and value is not None
            }
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

if __name__ == "__main__":
    if settings.PRODUCTION:
        StandaloneApplication(app, gunicorn_conf.options).run()
    else:
        uvicorn.run(app, host = settings.HOST, port = settings.PORT)
    #os.system("cd ./reactjs && bash start.sh")
