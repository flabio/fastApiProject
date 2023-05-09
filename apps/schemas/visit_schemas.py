from pydantic import BaseModel

class VisitSchema(BaseModel):
    visit_date:str
    visit_hora:str
    visit_description:str
    visit_status:str
    user_id:int
    is_active:bool=True
    