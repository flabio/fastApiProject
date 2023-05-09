from fastapi import HTTPException,status
from apps.model.visit_model import Visit
from apps.model.user_model import User
from sqlalchemy import func, extract, or_
from datetime import datetime
from apps.utils import config_page


class VisitedRepository:
    
    async def all_visited(payload,page:int,limite:int,db):
        try:
            count_query=db.query(Visit).join(User).\
                        filter(User.sub_detachment_id==payload.get("sub_detachment_id")).\
                        filter(User.church_id==payload.get("church_id")).count()
            page_offset= config_page.page_offset(page,limite)
            if limite==0:
                limite =10
                
            page_total= config_page.page_total_cell(count_query,limite)
            res=db.query(Visit.id,
                         Visit.visit_date,
                         Visit.visit_hora,
                         Visit.visit_description,
                         Visit.visit_status,
                         User.first_name+" "+User.last_name.label("full_name"),
                         ).\
                        join(User).\
                        filter(User.sub_detachment_id==payload.get("sub_detachment_id")).\
                        filter(User.church_id==payload.get("church_id")).\
                        order_by(Visit.id.desc()).\
                        offset(page_offset).limit(limite).all()
            return {"data":res,"page_total":page_total }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    async def all_visited_month(payload,db):
        try:
            
            result=db.query(Visit.id,
                         Visit.visit_date,
                         Visit.visit_hora,
                         Visit.visit_description,
                         Visit.visit_status,
                         User.first_name,
                         User.last_name,
                         ).\
                        join(User).\
                        filter(User.sub_detachment_id==payload.get("sub_detachment_id")).\
                        filter(User.church_id==payload.get("church_id")).\
                        filter( extract('month', (Visit.visit_date))==datetime.now().month).\
                        all()
            return result
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    async def create_visited(data,db):
        try:
            new_data=Visit(**data.dict())
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data":new_data,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e}")
        
    async def update_visited(id:int,data,db):
        try:
            result=db.query(Visit).filter(Visit.id==id)
            if not result.first() :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the rol is not a valid")
            result.update(data.dict(exclude_unset=True))
            db.commit()
            return {"data":data,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The id of the rol is not a valid")
    
    async def delete_visited_by_id(id:int,db):
        try:
            result=db.query(Visit).filter(Visit.id==id)
            if result.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the rol is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")
    
    