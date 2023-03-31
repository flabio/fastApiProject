
from pydantic import BaseModel

class CitySchema(BaseModel):
    name:str
    postal_code:str
    is_active:bool=True
    