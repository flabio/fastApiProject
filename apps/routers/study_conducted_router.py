from fastapi import APIRouter,Depends,status
from apps.schemas.study_conducted_schemas import StudyConductedSchema,StudyGraduateSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.study_conducted_repository import StudyConductedRepository
from apps.repository.study_graduate_repository import StudyGraduateRepository
from apps.auth import check_admin

study_conducted_router=APIRouter(
    prefix="/api/v1/study_conducted",
    tags=["study_conducted"]
)


#dependencies=[Depends(check_admin)],
@study_conducted_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_study_conducted(id:int,db:Session=Depends(get_db)):
    return await StudyConductedRepository.all_study_conducteds(id,db)
 
@study_conducted_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_study_conducted(data:StudyConductedSchema,db:Session=Depends(get_db)):
    return await  StudyConductedRepository.create_study_conducted(data,db)
    
@study_conducted_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_study_conducted(id:int,db:Session=Depends(get_db)):
    return await  StudyConductedRepository.delete_study_conducted_by_id(id,db)


@study_conducted_router.get("/graduate/{id}", status_code=status.HTTP_200_OK)
async def get_study_graduate(id:int,db:Session=Depends(get_db)):
    return await StudyGraduateRepository.all_study_graduates(id,db)
 
@study_conducted_router.post("/graduate", status_code=status.HTTP_201_CREATED)
async def create_study_graduate(data:StudyGraduateSchema,db:Session=Depends(get_db)):
    return await  StudyGraduateRepository.create_study_graduate(data,db)
    
@study_conducted_router.delete("/graduate/{id}",status_code=status.HTTP_200_OK)
async def delete_study_graduate(id:int,db:Session=Depends(get_db)):
    return await  StudyGraduateRepository.delete_study_graduate_by_id(id,db)