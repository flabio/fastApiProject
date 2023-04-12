from fastapi import APIRouter,Depends,status,HTTPException

from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.attendace_repository import AttendaceRepository
from apps.auth import check_comandant,oauth2_scheme,verify_token
from apps.schemas.attendace_schemas import AttendaceSchemas

from typing import Optional

attendace_router=APIRouter(
    prefix="/api/v1/attendace",
    tags=["attendace"]
)


@attendace_router.get("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def alld_scouts(id:int,page: Optional[int] = 1,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await AttendaceRepository.all_attendace(id,payload,page,db)
  

@attendace_router.post("/",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def create_scout(data:AttendaceSchemas,db:Session=Depends(get_db)):
    validata_data=data.dict()
  
    validate_fields(validata_data)
    await AttendaceRepository.exist_attendace(validata_data["user_id"],validata_data["initial_letter"],db)
    return await AttendaceRepository.create_attendace(data,db)

@attendace_router.delete("/{id}",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def delete_scout(id:int,db:Session=Depends(get_db)):
    return await AttendaceRepository.delete_attendace_by_id(id,db)
   

#method private
def validate_fields(data):
    str_initial=data["initial_letter"].split("-")
    if len(str_initial[0])!=3:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="Please validate. for example (NAV-A2T1S1)")
    if len(data["initial_letter"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The initial_letter is required. for example (NAV-A2T1S1)")
    if len(data["attendace_date"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The attendace date is required")
    if int(data["user_id"])<=0 :
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The id of scout is required")
    