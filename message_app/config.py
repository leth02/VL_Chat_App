import logging
import os
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

LOG_LEVEL = os.getenv("LOG_LEVEL")
