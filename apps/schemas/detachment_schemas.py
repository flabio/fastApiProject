from pydantic import BaseModel
from typing import Optional

class DetachmentSchema(BaseModel):
    name:str
    section:str
    numbers:int
    district:str
    church_id:int
    church_name:Optional[str]
    is_active:bool=True
    class Config:
        orm_mode=True


class DetachmentCreateSchema(BaseModel):
    name:str
    section:str
    numbers:int
    district:str
    church_id:int
    is_active:bool=True


