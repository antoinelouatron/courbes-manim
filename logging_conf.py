import logging.config
from pathlib import Path

config = {
    "version": 1,
    'disable_existing_loggers': False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%H:%M:%S"
            },
        "verbose": {
            "format": "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
            }
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": Path(__file__).resolve().parent / "creation.log",
            "backupCount": 3,
            "encoding": "utf-8",
            "maxBytes": 100000,
            "formatter": "simple",
            "delay": True
        }
    }
}
logging.config.dictConfig(config)
logger = logging.getLogger("creation_video")
