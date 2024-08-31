from fastapi import FastAPI, Request, Header, HTTPException

from api.dto import ClientRequest
from api.logging_middleware import LoggingMiddleware
from enums import MethodEnum
from config import API_KEY
from wireguard.wireguard_tool import WireguardTools

app = FastAPI()
app.add_middleware(LoggingMiddleware)  # type: ignore


@app.post("/api/v1/client/{clientId}", status_code=200)
async def add_client(request: Request, client_id: int, x_api_key: str = Header(None)):
    await _handle_request_util(request, client_id, x_api_key)


@app.delete("/api/v1/client/{clientId}", status_code=200)
async def remove_client(request: Request, client_id: int, x_api_key: str = Header(None)):
    await _handle_request_util(request, client_id, x_api_key)


async def _handle_request_util(request: Request, client_id: int, x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403)
    try:
        method = MethodEnum(value=request.method)
        body = await request.json()
        client_request = ClientRequest.parse_obj(body)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=400)
    success = WireguardTools.handle_client(client_id, client_request, method=method)
    if not success:
        raise HTTPException(status_code=400)
