
from pydantic import BaseModel



class RolSchema(BaseModel):
    name:str
    is_active:bool=True
    