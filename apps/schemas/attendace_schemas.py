from pydantic import BaseModel
from typing import Optional

class AttendaceSchemas(BaseModel):
   
    attendace_date:str
    notebook:bool=False
    bible:bool=False
    uniform:bool=False
    offering:bool=False
    initial_letter:str
    user_id:int
    is_active:bool=True
    