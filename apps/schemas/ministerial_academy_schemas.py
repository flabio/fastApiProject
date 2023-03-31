
from pydantic import BaseModel



class MinisterialAcademySchema(BaseModel):
    name:str
    is_active:bool=True
    

class MinisterialAcademyUserSchema(BaseModel):
    name:str
    date_academy:str
    place:str
    is_active:bool=True

class MinisterialAcademyUserSchema(BaseModel):
    date_academy:str
    place:str
    user_id:int
    ministerial_academy_id:int
    is_active:bool=True
    