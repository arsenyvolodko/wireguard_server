import logging
import subprocess

import config
from server.api.dto.client import AddClientsRequest, RemoveClientsRequest

logger = logging.getLogger(__name__)


class WireguardTools:

    @classmethod
    def add_clients(cls, add_clients_request: AddClientsRequest) -> bool:
        add_clients_cmd = cls._gen_add_client_cmd(add_clients_request)
        if success := cls._exec_cmd(add_clients_cmd):
            logger.info(f"Clients {add_clients_request} added")
        return success

    @classmethod
    def remove_clients(cls, remove_clients_reqeust: RemoveClientsRequest) -> bool:
        remove_clients_cmd = cls._gen_remove_client_cmd(remove_clients_reqeust)
        if success := cls._exec_cmd(remove_clients_cmd):
            logger.info(f"Clients {remove_clients_reqeust} removed")
        return success

    @staticmethod
    def _gen_add_client_cmd(add_clients_request: AddClientsRequest) -> str:
        cmds = [
            f"wg set {config.WG_CONFIG_NAME} peer {client.public_key} allowed-ips {client.ip}"
            for client in add_clients_request.clients
        ]
        return " && ".join(cmds)

    @staticmethod
    def _gen_remove_client_cmd(remove_clients_request: RemoveClientsRequest) -> str:
        cmds = [
            f"wg set {config.WG_CONFIG_NAME} peer {client.public_key} remove"
            for client in remove_clients_request.clients
        ]
        return " && ".join(cmds)

    @staticmethod
    def _exec_cmd(cmd: str) -> bool:

        full_cmd = (
            f"docker exec {config.WG_CONTAINER_NAME} bash -c '"
            f"{cmd} && "
            f"wg-quick save {config.WG_CONFIG_NAME} && "
            f"wg-quick down {config.WG_CONFIG_NAME} && "
            f"wg-quick up {config.WG_CONFIG_NAME}'"
        )

        result = subprocess.run(
            full_cmd, capture_output=True, text=True, shell=True
        )
        success = result.returncode == 0
        if not success:
            logger.error(f"Error executing command: {cmd}")
            logger.error(f"Shell returncode: {result.returncode}")
            logger.error(f"stderr: {result.stderr}")

        return success
