from pydantic import BaseModel
from typing import Optional

class SubDetachmentSchema(BaseModel):
    name:str
    image:Optional[str]
    is_active:bool=True





class SubDetachmentListSchema(BaseModel):
    id:int
    name:str
    image:str
    is_active:bool=True
    class Config():
        orm_mode=True