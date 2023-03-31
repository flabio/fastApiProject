from pydantic import BaseModel



class StudyConductedSchema(BaseModel):
    title_obtained:str
    semestre_numbre:int
    user_id:int
    is_active:bool=True
    
class StudyGraduateSchema(BaseModel):
    title_obtained:str
    type_name:str
    user_id:int
    is_active:bool=True

    
