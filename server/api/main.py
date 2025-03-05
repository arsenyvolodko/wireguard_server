from logging.config import dictConfig

from fastapi import FastAPI, Header, HTTPException

from server.api.dto.client import AddClientsRequest, AddClientRequest, RemoveClientsRequest, RemoveClientRequest
from server.core.logging import log_config
from server.enums import ActionEnum
from config import API_KEY
from wireguard.wireguard_tool import WireguardTools

app = FastAPI()
dictConfig(log_config)


@app.post("/api/v1/client/", status_code=201)
async def add_client(request_data: AddClientRequest, x_api_key: str = Header(None)):
    await _add_clients_util(request_data, x_api_key)


@app.delete("/api/v1/client/", status_code=204)
async def remove_client(request_data: RemoveClientRequest, x_api_key: str = Header(None)):
    await _remove_clients_util(request_data, x_api_key)


@app.post("/api/v1/clients/", status_code=201)
async def add_clients(request_data: AddClientsRequest, x_api_key: str = Header(None)):
    await _add_clients_util(request_data, x_api_key)


@app.delete("/api/v1/clients/", status_code=204)
async def remove_clients(request_data: RemoveClientsRequest, x_api_key: str = Header(None)):
    await _remove_clients_util(request_data, x_api_key)


def _check_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403)


async def _process_clients_util(
        request_data, x_api_key: str, action: str, single_model, batch_model, wg_method
):
    _check_api_key(x_api_key)

    if isinstance(request_data, single_model):
        request_data = batch_model(clients=[request_data])

    if not wg_method(request_data):
        raise HTTPException(status_code=400, detail=f"Failed to {action} clients")


async def _add_clients_util(request_data: AddClientRequest | AddClientsRequest, x_api_key: str):
    await _process_clients_util(
        request_data, x_api_key,
        action=ActionEnum.ADD,
        single_model=AddClientRequest,
        batch_model=AddClientsRequest,
        wg_method=WireguardTools.add_clients
    )


async def _remove_clients_util(request_data: RemoveClientRequest | RemoveClientsRequest, x_api_key: str):
    await _process_clients_util(
        request_data, x_api_key,
        action=ActionEnum.REMOVE,
        single_model=RemoveClientRequest,
        batch_model=RemoveClientsRequest,
        wg_method=WireguardTools.remove_clients
    )
