from fastapi import HTTPException,status
from apps.model.sub_detachment_model import SubDetachment
from apps.model.detachment_model import Detachment
import os
class SubDetachmentRepository:
    
    async def all_sub_detachments(db):
        try:
            return db.query(
                SubDetachment.id,
                SubDetachment.name,
                SubDetachment.image,
                SubDetachment.is_active,
                ).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                 detail=f"{e.args[0]}")
    
    async def get_sub_detachment_by_id(id:int,db):
        try:
            return db.query(
                SubDetachment.id,
                SubDetachment.name,
                SubDetachment.image,
         
                SubDetachment.is_active
                ).filter(SubDetachment.id==id).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                 detail=f"{e.args[0]}")
        
    async def create_sub_detachment(data,db):
        try:
            new_data=SubDetachment(**data)
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data":new_data,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                 detail=f"{e.args[0]}")

    async def update_sub_detachment(id:int,data,db):
        try:
            result=db.query(SubDetachment).filter(SubDetachment.id==id)
            if result.first()==None:
                raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
            
            result.update(data)
            db.commit()
            return {"data":data,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")
    
    async def delete_sub_detachment(id:int,db):
        try:
            result=db.query(SubDetachment).filter(SubDetachment.id == id)
            if result.first()==None:
                raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")
            
    
    #private methods
    async def exist_name(name:str,db):
        res = db.query(SubDetachment).filter(SubDetachment.name == name).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the name already exist")