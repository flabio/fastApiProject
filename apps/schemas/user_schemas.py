
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from faker import Faker
fake = Faker()

class UserSchema(BaseModel):
    first_name:str
    last_name:str
    identification:str
    type_identification:str
    expedition_date:str
    birth_day:str
    birth_place:str
    gender:str
    rh:str
    direction:str
    phone_number:Optional[str]
    cell_phone:str
    civil_status:str
    position:Optional[str]
    occupation:str
    school:int
    grade:int
    hobbies_interests:Optional[str]
    allergies:Optional[str]
    baptism_water:bool
    baptism_spirit:bool
    year_conversion:Optional[int]
    email:str
    password:Optional[str]
    rol_id:int
    church_id:int
    city_id:Optional[int]
    sub_detachment_id:Optional[int]
    is_active:bool    

class UserListSchema(BaseModel):
    id:int
    first_name:str
    last_name:str
    identification:str
    type_identification:str
    image:Optional[str]
    direction:Optional[str]
    cell_phone:Optional[str]
    phone_number:Optional[str]
    is_active:bool
    rol_name:str
    church_name:str
    class Config:
        orm_mode=True
    
class UserUpdateSchema(BaseModel):
    image:str=None
    first_name:str=None
    last_name:str=None
    identification:str=None
  
    email:str=None
    username:str=None
    rol_id:int=None
    is_active:bool=None
    


class ScoutSchema(BaseModel):
    image:Optional[str]
    first_name:str
    last_name:str
    identification:str
    type_identification:str
    direction:str
    cell_phone:str
    birth_day:str
    department_name:Optional[str]
    location_name:Optional[str]
    rh:str
    school_name:Optional[str]
    grade:int
    hobbies_interests:Optional[str]
    allergies:Optional[str]
    eps_name:Optional[str]
    email:Optional[str]=fake.email()
    password:str=fake.password()
    username:str=fake.email()
    rol_id:int=13
    church_id:Optional[int]
    city_id:Optional[int]
    sub_detachment_id:Optional[int]
    is_active:bool    

    
class UserByIdSchema(BaseModel):
    id:int
    first_name:str
    last_name:str
    image:Optional[str]
    identification:str
    type_identification:str
    expedition_date:Optional[str]
    birth_day:str
    birth_place:str
    gender:str
    rh:str
    direction:str
    phone_number:Optional[str]
    cell_phone:Optional[str]
    civil_status:Optional[str]
    position:Optional[str]
    occupation:Optional[str]
    school:Optional[int]
    grade:Optional[int]
    hobbies_interests:Optional[str]
    allergies:Optional[str]
    baptism_water:bool
    baptism_spirit:bool
    year_conversion:Optional[int]
    email:str
    rol_id:int
    church_id:int
    city_id:Optional[int]
    is_active:bool    
    rol_name:str
    church_name:str
    church_address:Optional[str]
    church_telephone:Optional[str]
    class Config():
        orm_mode=True

class AuthLonginSchema(BaseModel):
    username:str
    password:str
    class Config():
        orm_mode=True
        
class UserId(BaseModel):
    id:int