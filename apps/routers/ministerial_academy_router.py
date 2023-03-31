from fastapi import APIRouter,Depends,status,HTTPException

from  apps.schemas.ministerial_academy_schemas import MinisterialAcademySchema,MinisterialAcademyUserSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.model.ministerial_academy_model import MinisterialAcademy
from apps.repository.ministerial_academy_repository import MinisterialAcademyRepository
from apps.repository.user import UserRepository
from apps.auth import check_admin
from typing import Optional
ministerial_academy_router=APIRouter(
    prefix="/api/v1/ministerial_academy",
    tags=["ministerial_academy"]
)



#dependencies=[Depends(check_admin)],
@ministerial_academy_router.get("/", status_code=status.HTTP_200_OK)
async def read_ministerial_academys(db:Session=Depends(get_db)):
    return await MinisterialAcademyRepository.all_ministerial_academys(db)
 
@ministerial_academy_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_ministerial_academy(data:MinisterialAcademySchema,db:Session=Depends(get_db)):
    new_data =data.dict()
    
    _validate_fields(new_data)
    await MinisterialAcademyRepository.exist_name(new_data["name"],db)
    result=await MinisterialAcademyRepository.create_ministerial_academy(data,db)
    return result

@ministerial_academy_router.post("/create_ministerial_academy_user", status_code=status.HTTP_201_CREATED)
async def create_ministerial_academy_user(data:MinisterialAcademyUserSchema,db:Session=Depends(get_db)):
    new_data =data.dict()

    _validate_ministerial_academy_user_fields(new_data)
    await MinisterialAcademyRepository.not_exist_ministerial_academy_id(new_data["ministerial_academy_id"],db)
    await UserRepository.exist_id(new_data["user_id"],db)
    await MinisterialAcademyRepository.exist_ministerial_academy_user(new_data["user_id"],new_data["ministerial_academy_id"],db)
    return await MinisterialAcademyRepository.create_ministerial_academy_user(data,db)
    
@ministerial_academy_router.delete("/delete_ministerial_academy_user/{id}", status_code=status.HTTP_201_CREATED)
async def delete_ministerial_academy_user(id:int,db:Session=Depends(get_db)):
    return await MinisterialAcademyRepository.delete_ministerial_academy_user_by_id(id,db)
    
@ministerial_academy_router.get("/ministerial_academy_user/{id}", status_code=status.HTTP_200_OK)
async def read_ministerial_academys(id:int,db:Session=Depends(get_db)):
    return await MinisterialAcademyRepository.all_ministerial_academy_users(id,db)

@ministerial_academy_router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def update_ministerial_academy(id:int,data:MinisterialAcademySchema,db:Session=Depends(get_db)):
    new_data=data.dict()
    _validate_fields(new_data)
    if data.name!=new_data["name"]:
        await MinisterialAcademyRepository.exist_name(new_data["name"],db)
    
    return await  MinisterialAcademyRepository.update_ministerial_academy(id,data,db)

@ministerial_academy_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_ministerial_academy(id:int,db:Session=Depends(get_db)):
    return await  MinisterialAcademyRepository.delete_ministerial_academy_by_id(id,db)


def _validate_fields(new_data):
    if len(new_data["name"])==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="The name is required")
    


def _validate_ministerial_academy_user_fields(new_data):
    if len(new_data["date_academy"])==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="The date_academy is required")
    if len(new_data["place"])==0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="The place is required")
    
   
   