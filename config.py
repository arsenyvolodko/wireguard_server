import os

from dotenv import load_dotenv

load_dotenv(".env")

API_KEY: str = os.getenv("API_KEY")
WG_CONFIG_NAME: str = os.getenv("WG_CONFIG_NAME", "wg0")
WG_CONTAINER_NAME: str = os.getenv("WG_CONTAINER_NAME", "wireguard")
