from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.parentesco_model import Parentesco,Scoutkindred 
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.city_model import City
from apps.model.sub_detachment_model import SubDetachment
from apps.utils import config_page
from sqlalchemy import func,extract,or_
from faker import Faker
fake = Faker()
class ScoutRepository:

    async def all_scouts(payload:int,name:str,page:int,limite:int,db):
        try:
            payload.get("sub_detachment_id")
            search = "%{}%".format(name)
            count_query=db.query(User).join(Rol).join(Church).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id==13).count()
            page_offset= config_page.page_offset(page,limite)
        
            if limite==0:
                limite =10

            page_total= config_page.page_total_cell(count_query,limite)
            res = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.identification,
                    User.type_identification,
                    User.image,
                    User.birth_day,
                    User.cell_phone,
                    extract('year', func.age(User.birth_day)).label("age"),
                    Rol.name.label("rol_name"),
                    Church.name.label("church_name"),
                    SubDetachment.name.label("sub_detachment_name"),
                   SubDetachment.image.label("sub_detachment_image"),
                ).join(Rol).join(Church).join(SubDetachment).\
                    filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                    filter(User.church_id == payload.get("church_id")).\
                    filter(Rol.id==13).order_by(User.ceated_at.desc())
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else: 
                res= res.filter(or_( User.first_name.ilike(search) , User.last_name.ilike(search))).\
                    offset(page_offset).limit(limite).all()
            return {"data":res,"page_total":page_total }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def scout_find_by(id:int,payload,db):
        try:
            res = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.identification,
                    User.type_identification,
                    User.direction,
                    User.department_name,
                    User.location_name,
                    User.image,
                    User.birth_day,
                    User.cell_phone,
                    User.rh,
                    User.school_name,
                    User.grade,
                    User.hobbies_interests,
                    User.allergies,
                    User.eps_name,
                     extract('year', func.age(User.birth_day)).label("age"),
                    City.name.label("city_name"),
                    User.city_id,
                    Rol.name.label("rol_name"),
                    Church.name.label("church_name"),
                    SubDetachment.name.label("sub_detachment_name"),
                   SubDetachment.image.label("sub_detachment_image"),
                ).join(Rol).\
                  join(Church).\
                  join(SubDetachment).\
                  join(City).\
                  filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                  filter(User.church_id == payload.get("church_id")).\
                  filter(Rol.id==13).filter(User.id==id).first()
            
            query_kindred=db.query(
                Scoutkindred.id,
                Parentesco.first_name,
                Parentesco.last_name,
                Parentesco.cell_phone,
                Parentesco.direction,
                Parentesco.type_parentesco,
                Parentesco.identification,
                Parentesco.civil_status,
                ).join(Parentesco).filter(Scoutkindred.scout_id==id).all()
            return {"data":res ,'kindred':query_kindred}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    
    async def scout_find_by_id(id:int,payload,db):
        try:
            res = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.identification,
                    User.type_identification,
                    User.direction,
                    User.department_name,
                    User.location_name,
                    User.image,
                    User.birth_day,
                    User.cell_phone,
                    User.rh,
                    User.school_name,
                    User.grade,
                    User.hobbies_interests,
                    User.allergies,
                    User.city_id,
                    User.eps_name,
                ).join(Rol).join(Church).\
                    join(SubDetachment).\
                    join(City).\
                    filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                    filter(User.church_id == payload.get("church_id")).\
                    filter(Rol.id==13).\
                    filter(User.id==id).first()
            return {"data":res }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def create_scout(user,payload, db):
        try:
            new_user = User(**user)
            new_user.email=fake.email()
            new_user.sub_detachment_id=payload["sub_detachment_id"]
            new_user.church_id=payload["church_id"]
            new_user.rol_id=13
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"data": new_user, "detail": "the data was saved successfully"}
        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )
    async def edit_scout(id:int,payload ,data,db):
        try:
            result=db.query(User).filter(User.id==id)
            if result.first()==None:
                raise HTTPException(status_code=status.HTTP_400_BAD,detail="The id is not a valid")
         
            result.update(data)
            db.commit()
            return {"data":data,"detail":"the data was successfully updated"}

        except Exception as e:
           raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )
