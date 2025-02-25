from server.api.dto.extended_model import ExtendedBaseModel


class ClientRequest(ExtendedBaseModel):
    ip: str
