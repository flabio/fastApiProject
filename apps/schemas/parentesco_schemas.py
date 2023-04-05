from pydantic import BaseModel

class ParentescoSchema(BaseModel):
    id:int
    first_name:str
    last_name:str
    identification:str
    type_parentesco:str
    direction:str
    cell_phone:str
    civil_status:str
    is_active:bool=True    
    user_id:int
    
