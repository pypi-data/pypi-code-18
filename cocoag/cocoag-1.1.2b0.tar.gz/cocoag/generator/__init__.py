import logging.config
from cocoag.configuration.config import config

if config.getboolean("logging", "enable_logging"):
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": config.get("logging", "log_level"),
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": config.get("logging", "log_level"),
                "formatter": "simple",
                "filename": config.get("logging", "logging_output_file"),
                "maxBytes": 10485760,
                "backupCount": 20,
                "encoding": "utf8"
            }

        },
        "root": {
            "level": config.get("logging", "log_level"),
            "handlers": ["console", "file_handler"]
        }
    }

    logging.config.dictConfig(LOGGING_CONFIG)