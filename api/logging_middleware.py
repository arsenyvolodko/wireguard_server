from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from config import logger

LOGGER_MESSAGE = "{method} {url} {ip} {status_code}"


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        method = request.method
        url = str(request.url)

        response = await call_next(request)

        status_code = response.status_code
        logger.info(LOGGER_MESSAGE.format(method=method, url=url, ip=client_ip, status_code=status_code))

        return response
