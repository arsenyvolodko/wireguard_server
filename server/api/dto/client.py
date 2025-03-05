from server.api.dto.extended_model import ExtendedBaseModel


class AddClientRequest(ExtendedBaseModel):
    public_key: str
    ip: str


class RemoveClientRequest(ExtendedBaseModel):
    public_key: str


class AddClientsRequest(ExtendedBaseModel):
    clients: list[AddClientRequest]


class RemoveClientsRequest(ExtendedBaseModel):
    clients: list[RemoveClientRequest]
