from fastapi import APIRouter,Depends,status,HTTPException
from  apps.schemas.church_schemas import ChurchSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.church_repository import ChurchRepository
from apps.auth import check_admin
from typing import Optional
church_router=APIRouter(
    prefix="/api/v1/churchs",
    tags=["churchs"]
)


#@church_router.get("/", dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
@church_router.get("/",dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def get_churchs(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 5,db:Session=Depends(get_db)):
   
    return await ChurchRepository.all_churchs(q,page,limite,db)

@church_router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_church(id:int,db:Session=Depends(get_db)):
    return await ChurchRepository.find_church_by_id(id,db)
 
@church_router.post("/",status_code=status.HTTP_201_CREATED)
async def create_church(church:ChurchSchema,db:Session=Depends(get_db)):
    new_church =church.dict()
    validate_church_fields(new_church)
    
    await ChurchRepository.exist_name(new_church["name"],db)
    await ChurchRepository.exist_email(new_church["email"],db)
    result=await ChurchRepository.create_church(church,db)
    return result


@church_router.patch("/{id}",status_code=status.HTTP_201_CREATED)
async def update_church(id:int,church:ChurchSchema,db:Session=Depends(get_db)):
    new_church=church.dict()
    validate_church_fields(new_church)
    data  =await ChurchRepository.find_church_by_id(id,db)
    if data.name!=new_church["name"]:
        await ChurchRepository.exist_name(new_church["name"],db)
    if data.email!=new_church["email"]:
        await ChurchRepository.exist_email(new_church["email"],db)
    result=await ChurchRepository.update_church(id,church,db)
    return result

@church_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_church(id:int,db:Session=Depends(get_db)):
    return await  ChurchRepository.delete_church(id,db)

def validate_church_fields(new_church):
   
    if len(new_church["name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The name is required")
    if len(new_church["email"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The email is required")
    
    if len(new_church["address"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The address is required")
    if len(new_church["telephone"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The telephone is required")