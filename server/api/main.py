from logging.config import dictConfig

from fastapi import FastAPI, Request, Header, HTTPException

from server.api.dto import ClientRequest
from server.core.logging import log_config
from server.enums import MethodEnum
from config import API_KEY
from wireguard.wireguard_tool import WireguardTools

app = FastAPI()
dictConfig(log_config)


@app.post("/api/v1/client/{public_key}", status_code=201)
async def add_client(request: Request, public_key: str, x_api_key: str = Header(None)):
    await _handle_request_util(request, public_key, x_api_key)


@app.delete("/api/v1/client/{public_key}", status_code=204)
async def remove_client(request: Request, public_key: str, x_api_key: str = Header(None)):
    await _handle_request_util(request, public_key, x_api_key)


async def _handle_request_util(request: Request, public_key: str, x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403)

    try:
        method = MethodEnum(value=request.method)
        if method == MethodEnum.POST:
            body = await request.json()
            client_request = ClientRequest.parse_obj(body)
            success = WireguardTools.add_client(public_key, client_request)
        else:
            success = WireguardTools.remove_client(public_key)

    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)

    if not success:
        raise HTTPException(status_code=400)
