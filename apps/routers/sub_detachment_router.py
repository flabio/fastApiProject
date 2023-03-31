from fastapi import APIRouter,Depends,status,UploadFile,File,HTTPException
from sqlalchemy.orm import session  
from apps.schemas.sub_detachment_schemas import SubDetachmentListSchema,SubDetachmentSchema
from apps.config.db import get_db
from apps.repository.sub_detachment_repository import SubDetachmentRepository

from apps.auth import check_admin
from typing import List
from starlette.requests import Request
from apps.utils.profile_upload import update_upload_image_sub_detachment
import ast
import json
sub_detachment_router=APIRouter(
    prefix="/api/v1/sub_detachment",
    tags=["sub_detachment"],
    
)

@sub_detachment_router.get("/",response_model=List[SubDetachmentListSchema],status_code=status.HTTP_200_OK)
async def get_sub_detachments(db:session=Depends(get_db)):
    return await SubDetachmentRepository.all_sub_detachments(db)

@sub_detachment_router.get("/{id}", dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def get_sub_detachment(id:int,db:session=Depends(get_db)):
    return await SubDetachmentRepository.get_sub_detachment_by_id(id,db)

@sub_detachment_router.post("/",status_code=status.HTTP_201_CREATED)
async def create_sub_detachment(data:SubDetachmentSchema=Depends(),image: UploadFile = File(...),db:session=Depends(get_db)):
    validate_data=data.dict()
 
    if len(validate_data['name'])==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The name is required")

    filename= await update_upload_image_sub_detachment(image)
    
    await SubDetachmentRepository.exist_name(validate_data["name"],db)
    return  await SubDetachmentRepository.create_sub_detachment(data,filename,db)

@sub_detachment_router.post("/edit/{id}",status_code=status.HTTP_201_CREATED)
async def update_sub_detachment(id,request:Request,db:session=Depends(get_db)):
    form = await request.form()
    data = form.get("data").replace("'", "\"")
    validata_data = json.loads(data)

    if len(validata_data['name'])==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The name is required")

    if form!=None:
        if form['image']!="":
            filename= await update_upload_image_sub_detachment(form['image'])
            validata_data['image']=filename
        
    result= await SubDetachmentRepository.get_sub_detachment_by_id(id,db)
  
    if result==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The id is not found")
    
    if result.name!=validata_data['name']:
        await SubDetachmentRepository.exist_name(validata_data['name'],db)
    return await SubDetachmentRepository.update_sub_detachment(id,validata_data,db)

@sub_detachment_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_sub_detachment(id:int,db:session=Depends(get_db)):
    result= await SubDetachmentRepository.get_sub_detachment_by_id(id,db)
  
    if result==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The id is not found")
    
    return await SubDetachmentRepository.delete_sub_detachment(id,db)