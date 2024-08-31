import subprocess

from api.dto import ClientRequest
from enums import MethodEnum
from config import WG_CONFIG_PATH, SYNC_CONFIG_FILE_PATH, WG_CONFIG_NAME, logger


class WireguardTools:
    CONFIG_PATH = WG_CONFIG_PATH

    @classmethod
    def handle_client(cls, client_id: int, client_request: ClientRequest, method: MethodEnum) -> bool:
        client_data = cls._gen_client_data(client_id, client_request)
        cur_file_data = cls._get_data_from_server_file()

        try:
            if method == MethodEnum.POST:
                cls._add_wg_client(client_data)
            elif method == MethodEnum.DELETE:
                cls._remove_wg_client(cur_file_data, client_data)
        except Exception as err:
            logger.error(f"Error during handling client:\n{err}")
            cls._restore_data(cur_file_data)
            return False

        try:
            cls._sync_config()
        except Exception as err:
            logger.error(f"Error during syncing config:\n{err}")
            cls._restore_data(cur_file_data)
            return False

        return True

    @classmethod
    def _add_wg_client(cls, client_data: str):
        cur_data = cls._get_data_from_server_file()
        logger.info(f"Adding client:\n{cur_data}")
        if client_data in cur_data:
            logger.warning("Client data already exists in config")
            return
        with open(cls.CONFIG_PATH, "a") as file:
            file.write(client_data)
        logger.info("Client successfully added")

    @classmethod
    def _remove_wg_client(cls, cur_file_data: str, client_data: str):
        logger.info(f"Removing client:\n{client_data}")
        if client_data not in cur_file_data:
            logger.warning("No client data found in config")
            return

        new_data = cur_file_data.replace(client_data, "")
        cls._write_data(new_data)
        logger.info("Client successfully removed")

    @classmethod
    def _write_data(cls, file_data):
        with open(cls.CONFIG_PATH, "w") as file:
            file.write(file_data)

    @staticmethod
    def _gen_client_data(client_id: int, client_request: ClientRequest) -> str:
        client_name = f"{client_id}_{client_request.device_num}"
        new_data = (f"### Client {client_name}\n"
                    f"[Peer]\n"
                    f"PublicKey = {client_request.public_key}\n"
                    f"AllowedIPs = {client_request.ip}\n"
                    f"\n")
        return new_data

    @classmethod
    def _get_data_from_server_file(cls) -> str:
        with open(cls.CONFIG_PATH, "r") as file:
            data = file.read()
        return data

    @staticmethod
    def _sync_config():
        subprocess.check_call(
            f"{SYNC_CONFIG_FILE_PATH} {WG_CONFIG_NAME}",
            shell=True,
        )

    @classmethod
    def _restore_data(cls, data: str):
        try:
            cls._write_data(data)
            logger.info(f"Old data successfully restored")
        except Exception as err2:
            logger.error(f"Error during restoring data after error\n{err2}")
