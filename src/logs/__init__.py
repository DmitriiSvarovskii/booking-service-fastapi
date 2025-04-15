import os
import logging.config


log_directory = "/var/log/booking-service-fastapi"
os.makedirs(log_directory, exist_ok=True)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "info_filter": {
            "()": "logging.Filter",
            "name": ""
        },
        "error_filter": {
            "()": "logging.Filter",
            "name": ""
        }
    },

    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },

    "handlers": {
        "file_info": {
            "class": "logging.FileHandler",
            "filename": os.path.join(log_directory, "info.log"),
            "formatter": "default",
            "level": "INFO",
        },
        "file_error": {
            "class": "logging.FileHandler",
            "filename": os.path.join(log_directory, "error.log"),
            "formatter": "default",
            "level": "ERROR",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },

    "root": {
        "handlers": ["file_info", "file_error", "console"],
        "level": "INFO",
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
