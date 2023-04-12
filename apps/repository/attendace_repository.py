from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.attendance_model import Attendace
from apps.utils import config_page

class AttendaceRepository:

    async def all_attendace(id:int,payload,page:int,db):
        try:
            limite=5
            sub_detachment_id=payload["sub_detachment_id"]
            church_id=payload["church_id"]
            count_query=db.query(Attendace).join(User).\
                    filter(User.church_id==church_id).\
                    filter(User.sub_detachment_id == sub_detachment_id).\
                    filter(User.rol_id==13).filter(Attendace.user_id==id).count()
            page_offset= config_page.page_offset(page,limite)
           
            if limite==0:
                limite =5

            page_total= config_page.page_total_cell(count_query,limite)
            res = db.query(
                        Attendace.id,
                        Attendace.bible,
                        Attendace.offering,
                        Attendace.uniform,
                        Attendace.notebook,
                        Attendace.initial_letter,
                        Attendace.attendace_date
                ).join(User).filter(User.church_id==church_id).\
                    filter(User.sub_detachment_id == sub_detachment_id).\
                    filter(User.rol_id==13).filter(Attendace.user_id==id).order_by(Attendace.id.desc())
                    
            res= res.offset(page_offset).limit(limite).all()
            return {"data":res,"total_attendace":count_query,"page_total":page_total }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def create_attendace(data,db):
        try:
            new_data = Attendace(**data.dict())
            new_data.initial_letter= new_data.initial_letter.upper()
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data": new_data, "detail": "the data was saved successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args}"
            )
    async def delete_attendace_by_id(id:int,db):
        try:
            data=db.query(Attendace).filter(Attendace.id==id)
            if data.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id is not a valid")
            data.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")
    #private
            
            
    async def exist_attendace(user_id:int,initial_letter:str,db):
        res = db.query(Attendace).\
            filter(Attendace.initial_letter == initial_letter.upper()).\
            filter(Attendace.user_id == user_id).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="Your assistance is already assigned")