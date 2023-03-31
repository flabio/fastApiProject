from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.city_model import City
from apps.model.sub_detachment_model import SubDetachment
from apps.utils import config_page
from sqlalchemy import func

class ScoutRepository:

    async def all_scouts(sub_detachment_id:int,name:str,page:int,limite:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(User).join(Rol).join(Church).join(SubDetachment).filter(User.sub_detachment_id == sub_detachment_id).filter(Rol.id==13).count()
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
                    Rol.name.label("rol_name"),
                    Church.name.label("church_name"),
                    SubDetachment.name.label("sub_detachment_name"),
                   SubDetachment.image.label("sub_detachment_image"),
                ).join(Rol).join(Church).join(SubDetachment).filter(User.sub_detachment_id == sub_detachment_id).filter(Rol.id==13)
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else:    
                res= res.filter(User.first_name.ilike(search) ).offset(page_offset).limit(limite).all()
            return {"data":res,"page_total":page_total }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def scout_find_by(id:int,sub_detachment_id:int,db):
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
                    City.name.label("city_name"),
                    Rol.name.label("rol_name"),
                    Church.name.label("church_name"),
                    SubDetachment.name.label("sub_detachment_name"),
                   SubDetachment.image.label("sub_detachment_image"),
                ).join(Rol).join(Church).join(SubDetachment).join(City).filter(User.sub_detachment_id == sub_detachment_id).filter(Rol.id==13).filter(User.id==id).first()
            return {"data":res }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def create_user(user, db):
        try:
            new_user = User(**user.dict())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"data": new_user, "detail": "the data was saved successfully"}
        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )
