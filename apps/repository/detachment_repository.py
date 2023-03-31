from fastapi import HTTPException,status
from apps.model.detachment_model import Detachment
from apps.model.church_model import Church
from apps.utils import config_page
class DetachmentRepository:
    
    async def all_detachments(name:str,page:int,limite:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(Detachment).where(Detachment.church_id==Church.id).count()
            page_offset= config_page.page_offset(page,limite)
            
            if limite==0:
                limite =5
            
            page_total= config_page.page_total_cell(count_query,limite)
        
            res=db.query( Detachment.id,
                    Detachment.name,
                    Detachment.numbers,
                    Detachment.district,
                    Detachment.section,
                    Detachment.church_id,
                    Church.name.label("church_name")).where(Detachment.church_id==Church.id).order_by(Detachment.id.desc())
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else:    
                res= res.filter(Detachment.name.ilike(search)).offset(page_offset).limit(limite).all()
            
            return {"data":res,"page_total":page_total }
           
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")

    async def find_detachment_by_id(id:int,db):
        try:
            return db.query(Detachment).filter(Detachment.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
    
    async def create_detachment(detachment,db):
        try:
            new_detachment =Detachment(**detachment.dict())
            db.add(new_detachment)
            db.commit()
            db.refresh(new_detachment)
            return {"data": new_detachment, "msg": "the data was saved successfully"}
            
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
    
    async def update_detachment(id:int,detachment,db):
        try:
            result=db.query(Detachment).filter(Detachment.id==id)
            if result.first()==None:
                raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
            result.update(detachment.dict(exclude_unset=True))
            db.commit()
            return {"data": detachment, "msg": "the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
    
    async def delete_detachment(id:int,db):
        try:
            result=db.query(Detachment).filter(Detachment.id == id)
            if result.first() ==None:
                raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error deleting.....")
    
    #private methods
    async def exist_name(name:str,db):
        res = db.query(Detachment).filter(Detachment.name == name).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the name already exist")
    async def exist_numbers(numbers:str,db):
        res = db.query(Detachment).filter(Detachment.numbers == numbers).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the number already exist")