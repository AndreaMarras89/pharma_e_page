"""Main Entrypoint."""

import argparse

import gunicorn.app.base
from gunicorn.glogging import Logger
from loguru import logger

from backend.app import app
from backend.configuration import config


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """Gunicorn application."""

    def __init__(self, app, options=None):
        """Inits."""
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        """Loads the configuration."""
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        """Loads the Application."""
        return self.application


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=config.default_workers)
    parser.add_argument("--bind", type=str, default=f"0.0.0.0:{config.server_port}")
    parser.add_argument("--timeout", type=str, default=str(config.default_timeout))
    args = parser.parse_args()

    options = {
        "bind": args.bind,
        "workers": args.workers,
        "timeout": args.timeout,
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": Logger,
        "preload": True,
    }

    logger.info("Starting server")
    StandaloneApplication(app, options).run()
