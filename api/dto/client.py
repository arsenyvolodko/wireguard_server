from api.dto.extended_model import ExtendedBaseModel


class ClientRequest(ExtendedBaseModel):
    device_num: int
    public_key: str
    ip: str
