from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import session
from apps.schemas.detachment_schemas import DetachmentSchema,DetachmentCreateSchema
from apps.config.db import get_db
from apps.repository.detachment_repository import DetachmentRepository
from apps.auth import check_admin
from typing import Optional
detachment_router=APIRouter(
    prefix="/api/v1/detachment",
    tags=["detachment"],
)

@detachment_router.get("/", status_code=status.HTTP_200_OK)
async def get_detachments(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 5,db:session=Depends(get_db)):
    return await DetachmentRepository.all_detachments(q,page,limite,db)

@detachment_router.get("/{id}",status_code=status.HTTP_200_OK)
async def get_detachment(id:int,db:session=Depends(get_db)):
    return await DetachmentRepository.find_detachment_by_id(id,db)

@detachment_router.post("/",status_code=status.HTTP_201_CREATED)
async def add_detachment(detachment:DetachmentCreateSchema,db:session=Depends(get_db)):
    new_detachment = detachment.dict()
    
    _validate_detachment_fields(new_detachment)
    await DetachmentRepository.exist_name(new_detachment["name"],db)
    await DetachmentRepository.exist_numbers(new_detachment["numbers"],db)
    result=await DetachmentRepository.create_detachment(detachment,db)
    return result

@detachment_router.patch("/{id}",status_code=status.HTTP_201_CREATED)
async def get_detachment(id:int,detachment:DetachmentSchema,db:session=Depends(get_db)):
    new_detachment = detachment.dict()
    _validate_detachment_fields(new_detachment)
    data= await DetachmentRepository.find_detachment_by_id(id,db)
    if data.name!=new_detachment["name"]:
        await DetachmentRepository.exist_name(new_detachment["name"],db)
    
    
    if data.numbers!=new_detachment["numbers"]:
        await DetachmentRepository.exist_numbers(new_detachment["numbers"],db)
        
    result=await DetachmentRepository.update_detachment(id,detachment,db)
    return result

@detachment_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_detachment(id:int,db:session=Depends(get_db)):
    return await DetachmentRepository.delete_detachment(id,db)

def _validate_detachment_fields(new_detachment):
    if len(new_detachment["name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The name is required")
    
    if new_detachment["numbers"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The numbers is required")
        
    if len(new_detachment["section"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The section is required")
    
    if len(new_detachment["district"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The district is required")
    