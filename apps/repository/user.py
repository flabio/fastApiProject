from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.detachment_model import Detachment
from apps.model.sub_detachment_model import SubDetachment
from apps.model.ministerial_academy_user import MinisterialAcademyUser
from apps.model.ministerial_academy_model import MinisterialAcademy
from apps.auth import get_password_hash
from apps.utils import config_page
from sqlalchemy import func, extract, or_
from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import datetime
env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

class UserRepository:

    async def all_users(name:str,page:int,limite:int,rol:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(User).count()
            if limite==0:
                limite =10
              
            page_offset= config_page.page_offset(page,limite)
            page_total= config_page.page_total_cell(count_query,limite)
           
            res = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.identification,
                    User.type_identification,
                    User.image,
                    User.is_active,
                    User.direction,
                    User.cell_phone,
                    User.phone_number,
                    Rol.name.label("rol_name"),
                    Church.name.label("church_name"),
                ).where(User.rol_id == Rol.id).where(User.church_id == Church.id).order_by(User.id.desc())
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else:
                if rol>0:
                    res = res.filter(User.rol_id==rol).filter(or_(User.first_name.ilike(search), User.last_name.ilike(search))).\
                        offset(page_offset).limit(limite).all()
                else:
                    res = res.filter(or_(User.first_name.ilike(search), User.last_name.ilike(search))).\
                       offset(page_offset).limit(limite).all()
                
            return {"data":res,"page_total":page_total,"page":page_offset }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )

    async def find_user_by_id(id: int, db):
        try:
            user = db.query(User.id,
                User.first_name,
                User.last_name,
                User.image,
                User.identification,
                User.type_identification,
                User.expedition_date,
                User.birth_day,
                User.birth_place,
                User.gender,
                User.rh,
                User.direction,
                User.phone_number,
                User.cell_phone,
                User.civil_status,
                User.position,
                User.occupation,
                User.school,
                User.grade,
                User.hobbies_interests,
                User.allergies,
                User.baptism_water,
                User.baptism_spirit,
                User.year_conversion,
                User.email,
                User.rol_id,
                User.church_id,
                User.city_id,
                User.is_active,    
                Rol.name.label("rol_name"),
                User.sub_detachment_id
                ).filter(User.id == id).where(User.rol_id == Rol.id).where(User.church_id == Church.id).first()
            detachment=db.query(Detachment.id,Detachment.name,Detachment.numbers,Detachment.district,Detachment.section).filter(Detachment.church_id ==user.church_id).first()
            church=db.query(  User.first_name,
                User.last_name,Church.name.label("church_name"),
                Church.address.label("church_address"),
                Church.telephone.label("church_telephone")).join(Church).join(Rol).\
                filter(Church.id ==user.church_id).\
                filter(Rol.id==11).\
                first()
       
            sub_detachment=db.query(SubDetachment.name,SubDetachment.image).filter(SubDetachment.id ==user.sub_detachment_id).first()
           
            ministerial_academy_user=db.query(
                                            MinisterialAcademyUser.id,
                                            MinisterialAcademyUser.date_academy,
                                            MinisterialAcademyUser.place,
                                            MinisterialAcademy.name
                                            ).where(MinisterialAcademyUser.ministerial_academy_id==MinisterialAcademy.id).where(MinisterialAcademyUser.user_id==id).all()
          
            return [{"user":user,"church":church,"detachment":detachment,"sub_detachment":sub_detachment,"ministerial_academy_user":ministerial_academy_user}]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")

    async def create_user(user, db):
        try:
            new_user = User(**user.dict())
            new_user.username=new_user.identification
            new_user.password = get_password_hash(new_user.password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"data": new_user, "detail": "the data was saved successfully"}
        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )

    async def update_by_image_user(id, file, db):
        try:
            user = db.query(User.image).filter(User.id == id).first()
            if user[0]!=None:
                img=user[0].split("/")[5]
                remove_file = Path(os.getenv('FILEPATH')+img)
                remove_file.unlink(missing_ok=True)
            #remove_exist(user)
            db.query(User).filter(User.id == id).update(
                {User.image: file}, synchronize_session=False)
            db.commit()
            user_data = db.query(User.image).filter(User.id == id).first()
            return {"profile": user_data, "detail": "changed profile picture successfully"}
        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The format is not a valid"
            )

    async def update_user(id: int, user_update, db):
        try:
            user = db.query(User).filter(User.id == id)
            if not user.first():
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the user is not a valid")
            user.first().username=user_update.identification
            user.update(user_update.dict(exclude_unset=True))
            db.commit()
            return {"data":user_update,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The id of the user is not a valid")
    
    async def update_password_user(id, data, db):
        try:
            result = db.query(User).filter(User.id == id).\
                filter(User.id == id).first()
            if result == None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id is not a valid")
            result.password = get_password_hash(data.password)
            db.commit()
            db.refresh(result)
            return {"detail":"the password was updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The id of the user is not a valid")
    async def delete_user_by_id(id: int, db):
        try:
            user = db.query(User).filter(User.id == id)
            if user.first() is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the user is not a valid")
            user.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The id of the user is not a valid")

    async def birth_day_commenders(payload,db):
        try:
            result = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.image,
                    SubDetachment.image.label("sub_detachment_image"),
                    Rol.name.label("rol_name"),
                    User.birth_day,
                    extract('month', (User.birth_day)).label("mes"),
                    extract('day', (User.birth_day)).label("dia"),
                    
                ).join(Rol).join(Church).join(SubDetachment).\
                    filter(User.rol_id==12).\
                    filter(User.church_id==payload.get("church_id")).\
                    filter( extract('month', (User.birth_day))==datetime.now().month).\
                    all()
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def birth_day_scouts(payload,db):
        try:
            result = db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.image,
                    SubDetachment.image.label("sub_detachment_image"),
                    Rol.name.label("rol_name"),
                    User.birth_day,
                    extract('month', (User.birth_day)).label("mes"),
                    extract('day', (User.birth_day)).label("dia"),
                    
                ).join(Rol).join(Church).join(SubDetachment).\
                    filter(User.rol_id==13).\
                    filter(User.church_id==payload.get("church_id")).\
                    filter(User.sub_detachment_id==payload.get("sub_detachment_id")).\
                    filter( extract('month', (User.birth_day))==datetime.now().month).\
                    all()
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    # private

    async def exist_id(id: int, db):
        user = db.query(User).filter(User.id == id).first()
   
        if user == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The id of the user is not a valid")
    


    def exist_identification(identification:str, db):
        user = db.query(User).filter(
            User.identification == identification).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="identification already exist")

    def exist_email(email:str, db):
        user = db.query(User).filter(User.email == email).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="email already exist")
