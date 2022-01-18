import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import traceback
import os

from .config import LOG_LEVEL

LOG_DIRECTORY_PATH = os.path.dirname(__file__) + "/log"
LOG_FILE_PATH = LOG_DIRECTORY_PATH + "/message_app.log"

def create_log_file():
    Path(LOG_DIRECTORY_PATH).mkdir(exist_ok=True)
    Path(LOG_FILE_PATH).touch(exist_ok=True)

def configure_logging():
    logging.basicConfig(level=LOG_LEVEL)

def get_logger(name):
    logger = logging.getLogger(__name__)
    configure_logging()
    create_log_file()
    handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=100000, backupCount=3)
    logger.addHandler(handler)

    return logger