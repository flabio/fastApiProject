from fastapi import APIRouter,Depends,status,HTTPException

from  apps.schemas.rol_schemas import RolSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.model.rol_model import Rol
from apps.repository.rol_repository import RolRepository
from apps.auth import check_admin
from typing import Optional
rol_router=APIRouter(
    prefix="/api/v1/rols",
    tags=["rols"]
)
rols=[]


#dependencies=[Depends(check_admin)],
@rol_router.get("/", status_code=status.HTTP_200_OK)
async def read_rols(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 5,db:Session=Depends(get_db)):
    return await RolRepository.all_rols(q,page,limite,db)
 
@rol_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_rol(rol:RolSchema,db:Session=Depends(get_db)):
    new_rol =rol.dict()
    if len(new_rol["name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The name is required")
    await RolRepository.exist_name(new_rol["name"],db)
    result=await  RolRepository.create_rol(rol,db)
    return result


@rol_router.patch("/{id}", status_code=status.HTTP_201_CREATED)
async def update_rol(id:int,rol:RolSchema,db:Session=Depends(get_db)):
    new_rol=rol.dict()
    if len(new_rol["name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The name is required")
    data = await RolRepository.find_rol_by_id(id,db)
    if data.name!=new_rol["name"]:
        await RolRepository.exist_name(new_rol["name"],db)
    result=await  RolRepository.update_rol(id,rol,db)
    return result

@rol_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_rol(id:int,db:Session=Depends(get_db)):
    return await  RolRepository.delete_rol_by_id(id,db)
    