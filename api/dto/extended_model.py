import humps
from pydantic import BaseModel


class ExtendedBaseModel(BaseModel):

    class Config:
        alias_generator = humps.camelize
        populate_by_name = True
