from pydantic import BaseModel
from typing import Optional

class ParentescoSchema(BaseModel):
    id:Optional[int]
    first_name:str
    last_name:str
    identification:str
    type_parentesco:str
    direction:str
    cell_phone:str
    civil_status:str
    is_active:bool=True    
  
    
class ScoutKindredSchema(BaseModel):
    id:Optional[int]
    parentesco_id:int
    scout_id:int
    is_active:bool=True 