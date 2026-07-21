import logging
import sys

from pythonjsonlogger import jsonlogger

from app.core.settings import settings


def setup_logging():
    logger = logging.getLogger()

    logger.setLevel(settings.log_level)

    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)

    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)
