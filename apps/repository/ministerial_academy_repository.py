from fastapi import HTTPException,status
from apps.model.ministerial_academy_model import MinisterialAcademy
from apps.model.ministerial_academy_user import MinisterialAcademyUser


class MinisterialAcademyRepository:
    
    async def all_ministerial_academys(db):
        try:
            res=db.query(MinisterialAcademy).order_by(MinisterialAcademy.id.desc()).all()
            return {"data":res }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    async def find_ministerial_academy_by_id(id:int,db):
        try:
            return db.query(MinisterialAcademy).filter(MinisterialAcademy.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")
    
    async def create_ministerial_academy(data,db):
        try:
            result=MinisterialAcademy(**data.dict())
            db.add(result)
            db.commit()
            db.refresh(result)
            return {"data":result,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
        
    async def update_ministerial_academy(id:int,data,db):
        try:
            result=db.query(MinisterialAcademy).filter(MinisterialAcademy.id==id)
            if not result.first() :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the rol is not a valid")
            result.update(data.dict(exclude_unset=True))
            db.commit()
            return {"data":data,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The id of the rol is not a valid")
    
    async def delete_ministerial_academy_by_id(id:int,db):
        try:
            result=db.query(MinisterialAcademy).filter(MinisterialAcademy.id==id)
            if result.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the rol is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")

    #user ministerial academy
    async def all_ministerial_academy_users(id:int,db):
        try:
            ministerial_academy_user=db.query(
                                            MinisterialAcademyUser.id,
                                            MinisterialAcademyUser.date_academy,
                                            MinisterialAcademyUser.place,
                                            MinisterialAcademy.name
                                            
                                              ).where(MinisterialAcademyUser.ministerial_academy_id==MinisterialAcademy.id).where(MinisterialAcademyUser.user_id==id).all()
            return {"data":ministerial_academy_user }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
   
    async def create_ministerial_academy_user(data,db):
        try:
            result=MinisterialAcademyUser(**data.dict())
            db.add(result)
            db.commit()
            db.refresh(result)
            return {"data":result,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    async def delete_ministerial_academy_user_by_id(id:int,db):
        try:
            result=db.query(MinisterialAcademyUser).filter(MinisterialAcademyUser.id==id)
            if result.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")

    async def exist_ministerial_academy_user(user_id:int,id:int,db):
        result = db.query(MinisterialAcademy).where(MinisterialAcademyUser.ministerial_academy_id==id).where(MinisterialAcademyUser.user_id==user_id).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the ministerial academy already exists")
    #private methods
    async def exist_name(name:str,db):
        result = db.query(MinisterialAcademy).filter(MinisterialAcademy.name == name).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the name already exist")
    
    async def exist_ministerial_academy_id(id:str,db):
        result = db.query(MinisterialAcademy).filter(MinisterialAcademy.id == id).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the id of ministerial academy already exist")
    
    async def not_exist_ministerial_academy_id(id:str,db):
        result = db.query(MinisterialAcademy).filter(MinisterialAcademy.id == id).first()
        if result==None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the id of ministerial academy not exist")
