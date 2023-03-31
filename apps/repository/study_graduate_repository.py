from fastapi import HTTPException,status
from apps.model.study_conducted_model import StudyGraduate


class StudyGraduateRepository:
    
    async def all_study_graduates(user_id:int,db):
        try:
            results=db.query(StudyGraduate).where(StudyGraduate.user_id==user_id).all()
            return {"data":results }
           
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    
    async def create_study_graduate(data,db):
        try:
            new_data=StudyGraduate(**data.dict())
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data":new_data,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
        
    
    async def delete_study_graduate_by_id(id:int,db):
        try:
            rol=db.query(StudyGraduate).filter(StudyGraduate.id==id)
            if rol.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the rol is not a valid")
            rol.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")
    
    