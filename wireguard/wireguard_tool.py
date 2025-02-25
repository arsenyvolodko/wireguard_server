import logging
import subprocess

import config
from server.api.dto import ClientRequest

logger = logging.getLogger(__name__)


class WireguardTools:

    @classmethod
    def add_client(cls, public_key: str, client_request: ClientRequest) -> bool:
        add_client_cmd = cls._gen_add_client_cmd(public_key, client_request.ip)
        if success := cls._exec_cmd(add_client_cmd):
            logger.info(f"Client {public_key} added with ip {client_request.ip}")
        return success

    @classmethod
    def remove_client(cls, public_key: str) -> bool:
        remove_client_cmd = cls._gen_remove_client_cmd(public_key)
        if success := cls._exec_cmd(remove_client_cmd):
            logger.info(f"Client {public_key} removed")
        return success

    @staticmethod
    def _gen_add_client_cmd(public_key: str, ip: str) -> str:
        return f"wg set {config.WG_CONFIG_NAME} peer {public_key} allowed-ips {ip}"

    @staticmethod
    def _gen_remove_client_cmd(public_key: str) -> str:
        return f"wg set {config.WG_CONFIG_NAME} peer {public_key} remove"

    @staticmethod
    def _exec_cmd(cmd: str) -> bool:
        full_cmd = (f"bash -c 'docker exec {config.WG_CONTAINER_NAME} {cmd} && "
                    f"docker exec {config.WG_CONTAINER_NAME} wg-quick save {config.WG_CONFIG_NAME}'")
        result = subprocess.run(
            full_cmd, capture_output=True, text=True, shell=True
        )
        success = result.returncode == 0
        if not success:
            logger.error(f"Error executing command: {cmd}")
            logger.error(f"Shell returncode: {result.returncode}")
            logger.error(f"stderr: {result.stderr}")

        return success
