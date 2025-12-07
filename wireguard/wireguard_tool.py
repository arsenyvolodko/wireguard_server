import logging

import docker

import config
from server.api.dto.client import AddClientsRequest, RemoveClientsRequest

logger = logging.getLogger(__name__)
client = docker.from_env()


class WireguardTools:

    @classmethod
    def add_clients(cls, add_clients_request: AddClientsRequest) -> bool:
        add_clients_cmd = cls._gen_add_client_cmd(add_clients_request)
        success, logs = cls.exec_in_wireguard(add_clients_cmd)
        if not success:
            logger.error(
                f"Failed to execute add clients command in wireguard container. Error: {logs}"
            )
        return success

    @classmethod
    def remove_clients(cls, remove_clients_reqeust: RemoveClientsRequest) -> bool:
        remove_clients_cmd = cls._gen_remove_client_cmd(remove_clients_reqeust)
        success, logs = cls.exec_in_wireguard(remove_clients_cmd)
        if not success:
            logger.error(
                f"Failed to execute remove clients command in wireguard container. Error: {logs}"
            )
        return success

    @staticmethod
    def _gen_add_client_cmd(add_clients_request: AddClientsRequest) -> str:
        cmds = [
            f"wg set {config.WG_CONFIG_NAME} peer {client.public_key} allowed-ips {client.ip}"
            for client in add_clients_request.clients
        ]
        return "\n".join(cmds)

    @staticmethod
    def _gen_remove_client_cmd(remove_clients_request: RemoveClientsRequest) -> str:
        cmds = [
            f"wg set {config.WG_CONFIG_NAME} peer {client.public_key} remove"
            for client in remove_clients_request.clients
        ]
        return "\n".join(cmds)

    @staticmethod
    def exec_in_wireguard(main_cmd: str, *, timeout: int = 30) -> tuple[bool, str]:
        container = client.containers.get(config.WG_CONTAINER_NAME)

        exec_cmds = (f"wg-quick save {config.WG_CONFIG_NAME}\n"
                     f"wg-quick down {config.WG_CONFIG_NAME}\n"
                     f"wg-quick up {config.WG_CONFIG_NAME}")

        main_cmd += f"\n{exec_cmds}"

        cmd = ["sh", "-lc", main_cmd]

        res = container.exec_run(
            cmd,
            stdout=True,
            stderr=True,
            tty=False,
            privileged=True,
            user="root",
            demux=False,
        )

        output = (
            res.output.decode("utf-8", errors="replace")
            if isinstance(res.output, (bytes, bytearray))
            else str(res.output)
        )
        return res.exit_code == 0, output
