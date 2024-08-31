import logging
import os

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv(".env")

API_KEY: str = os.getenv("API_KEY")

WG_CONFIG_NAME: str = os.getenv("WG_CONFIG_NAME")
WG_CONFIG_PATH: str = os.getenv("WG_CONFIG_PATH")
SYNC_CONFIG_FILE_PATH: str = os.getenv("SYNC_CONFIG_FILE_PATH")
