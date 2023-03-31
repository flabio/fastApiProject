
from pydantic import BaseModel

class ChurchSchema(BaseModel):
    name:str
    email:str
    address:str
    telephone:str
    is_active:bool=True

class ChurchPaginatioSchema(BaseModel):
    id:int
    name:str
    email:str
    address:str
    telephone:str
    is_active:bool=True
    