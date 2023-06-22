from fastapi import APIRouter,Depends,status,HTTPException

from  apps.schemas.visit_schemas import VisitSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 

from apps.repository.visited_repository import VisitedRepository
from apps.auth import check_admin,check_comandant,verify_token,oauth2_scheme
from typing import Optional
visit_router=APIRouter(
    prefix="/api/v1/visit",
    tags=["visits"]
)
@visit_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def list_visits(q:Optional[str],page: Optional[int] = 1,limite: Optional[int] = 10,token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=verify_token(token)
    return await VisitedRepository.all_visited(payload,q,page,limite,db)

@visit_router.get("/not_scout_visit/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def list_visits(q:Optional[str],page: Optional[int] = 1,limite: Optional[int] = 10,token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=verify_token(token)
    return await VisitedRepository.all_not_user_visited(payload,q,page,limite,db)

@visit_router.get("/visit_month/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def list_visits_month(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=verify_token(token)
    return await VisitedRepository.all_visited_month(payload,db)
 
@visit_router.post("/",dependencies=[Depends(check_admin)], status_code=status.HTTP_201_CREATED)
async def create_visit(data:VisitSchema,db:Session=Depends(get_db)):
    if len(data.visit_date)==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="La fecha de la visita es requerida")
    if len(data.visit_hora)==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="La hora de la visita es requerida")
    
    
    if len(data.visit_description)==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="La descripción de la visita es requerida")
        
    if data.visit_status==None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="El estado de la visita es requerida")    
        
    return await  VisitedRepository.create_visited(data,db)
    


@visit_router.patch("/{id}",dependencies=[Depends(check_admin)], status_code=status.HTTP_201_CREATED)
async def update_visit(id:int,data:VisitSchema,db:Session=Depends(get_db)):
    new_data=data.dict()

    return await  VisitedRepository.update_visited(id,data,db)
    
@visit_router.delete("/{id}",dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def delete_visit(id:int,db:Session=Depends(get_db)):
    return await  VisitedRepository.delete_visited_by_id(id,db)
    