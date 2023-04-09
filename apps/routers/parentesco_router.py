from fastapi import APIRouter,Depends,status,HTTPException
from  apps.schemas.parentesco_schemas   import ParentescoSchema,ScoutKindredSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.parentesco_repository import ParentescoRepository
from apps.auth import check_comandant
from typing import Optional
parentesco_router=APIRouter(
    prefix="/api/v1/kindred",
    tags=["kindred"]
)


@parentesco_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def read_parentesco(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 10,db:Session=Depends(get_db)):
    return await ParentescoRepository.all_parentesco(q,page,limite,db)

@parentesco_router.get("/find_parentesco_by_id/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def find_parentesco_by_id(id:int,db:Session=Depends(get_db)):
    await ParentescoRepository.exist_id(id,db)
    return await ParentescoRepository.find_parentesco_by_id(id,db)


@parentesco_router.post("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_201_CREATED)
async def create_parentesco( data:ParentescoSchema,db:Session=Depends(get_db)):
    new_data=data.dict()
    _validates_fields(new_data)
    ParentescoRepository.exist_identification(new_data["identification"],db)
    return await ParentescoRepository.create_parentesco(data,db)
    
@parentesco_router.patch("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_201_CREATED)
async def update_parentesco(id:int, data:ParentescoSchema,db:Session=Depends(get_db)):
    new_data=data.dict()
    _validates_fields(new_data)
    return await ParentescoRepository.update_parentesco(id,data,db)

@parentesco_router.delete("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def delete_parentesco_by_id(id:int,db:Session=Depends(get_db)):
    return await ParentescoRepository.delete_parentesco_by_id(id,db)


@parentesco_router.post("/add_scout_kindred/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_201_CREATED)
async def add_scout_kindred( data:ScoutKindredSchema,db:Session=Depends(get_db)):
    new_data=data.dict()
    if new_data["parentesco_id"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The id of kindred is required")
    if new_data["scout_id"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The id of socut is required")
  
    await ParentescoRepository.exist_kindred(new_data["scout_id"],new_data["parentesco_id"],db)
    return await ParentescoRepository.add_scout_kindred(data,db)

@parentesco_router.delete("/delete_scout_kindred/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def delete_scout_kindred_by_id(id:int,db:Session=Depends(get_db)):
    return await ParentescoRepository.delete_scout_kindred_by_id(id,db)

def _validates_fields(data):
    if len(data["first_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The first name is required")
    
    if len(data["last_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The last name is required")
    
    if len(data["identification"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The identification is required")
    
    if data["type_parentesco"]=="" or data["type_parentesco"]==None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The type identification is required")
    
    if len(data["direction"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if len(data["cell_phone"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The cell phone is required")
    
    if len(data["civil_status"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The civil status is required")
   