from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.parentesco_model import Parentesco, Scoutkindred
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.city_model import City
from apps.model.sub_detachment_model import SubDetachment
from apps.utils import config_page
from sqlalchemy import func, extract, or_,cast, Date
from datetime import datetime
from faker import Faker

fake = Faker()


class ScoutRepository:

    async def all_scouts(payload: int, name: str, page: int, limite: int, age: int, db):
        try:
            payload.get("sub_detachment_id")
            search = "%{}%".format(name)
            count_query = db.query(User).join(Rol).join(Church).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).count()
            page_offset = config_page.page_offset(page, limite)

            if limite == 0:
                limite = 10

            page_total = config_page.page_total_cell(count_query, limite)
            res = db.query(
                User.id,
                User.first_name,
                User.last_name,
                User.identification,
                User.type_identification,
                User.image,
                User.birth_day,
                User.cell_phone,
                User.sub_detachment_id,
                User.ceated_at,
                extract('year', func.age(User.birth_day)).label("age"),
          
                Rol.name.label("rol_name"),
                Church.name.label("church_name"),
                SubDetachment.name.label("sub_detachment_name"),
                SubDetachment.image.label("sub_detachment_image"),
                
            ).join(Rol).join(Church).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).\
                order_by(User.ceated_at.asc())
                
                # filter(Rol.id == 13).filter(extract('day', func.age(cast(User.ceated_at, Date)))>=15).\
                # filter(extract('month', func.age(cast(User.ceated_at, Date)))==0).\
                        
            if name == None:
                res = res.offset(page_offset).limit(limite).all()

            else:
                
                if age > 0:
                    print(age)
                    res = res.filter(or_(User.first_name.ilike(search), User.last_name.ilike(search))).\
                        filter(extract('year', func.age(User.birth_day)) == age).\
                        offset(page_offset).limit(limite).all()
                else:
                    res = res.filter(or_(User.first_name.ilike(search), User.last_name.ilike(search))).\
                        offset(page_offset).limit(limite).all()
                    print(res)
            return {"data": res, "page_total": page_total}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    
    async def all_scouts_age(payload,  db):
        try:
            payload.get("sub_detachment_id")
            data=[]
            if payload.get("sub_detachment_id")==1:
                data=[8,9,10]
            if payload.get("sub_detachment_id")==2:
                data=[11,12,13]
            if payload.get("sub_detachment_id")==3:
                data=[14,15,16,17]
            if payload.get("sub_detachment_id")==9:
                data=[18,19,20,21]
            count_query = db.query(User).join(Rol).join(Church).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).count()
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
                extract('day', func.age(User.birth_day)).label("dias"),
                Rol.name.label("rol_name"),
                Church.name.label("church_name"),
                SubDetachment.name.label("sub_detachment_name"),
                SubDetachment.image.label("sub_detachment_image"),
            ).join(Rol).join(Church).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).\
                filter(extract('year', func.age(User.birth_day)).in_(data)).\
                order_by(User.ceated_at.desc()).\
                all()
            return {"data": res, "total_scout": count_query}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def scout_find_by(id: int, payload, db):
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
                filter(Rol.id == 13).filter(User.id == id).first()

            query_kindred = db.query(
                Scoutkindred.id,
                Parentesco.first_name,
                Parentesco.last_name,
                Parentesco.cell_phone,
                Parentesco.direction,
                Parentesco.type_parentesco,
                Parentesco.identification,
                Parentesco.civil_status,
            ).join(Parentesco).filter(Scoutkindred.scout_id == id).all()
            return {"data": res, 'kindred': query_kindred}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )

    async def scout_change_to_sub_detachment(payload, db):
        try:
            data=[]
            if payload.get("sub_detachment_id")==1:
                data=[8,9,10]
            if payload.get("sub_detachment_id")==2:
                data=[11,12,13]
            if payload.get("sub_detachment_id")==3:
                data=[14,15,16,17]
            if payload.get("sub_detachment_id")==9:
                data=[18,19,20,21]
            count_query = db.query(User).join(Rol).\
                join(Church).\
                join(SubDetachment).\
                join(City).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
              filter(extract('year', func.age(User.birth_day)).in_(data)).\
                filter(Rol.id == 13).count()
            result = db.query(
                User.id,
                User.image,
                User.first_name,
                User.last_name,
                User.birth_day,
                extract('year', func.age(User.birth_day)).label("age"),
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
                filter(extract('year', func.age(User.birth_day)).in_(data)).\
                filter(Rol.id == 13).limit(4).all()

            return {"data": result, 'total_scout': count_query}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )

    async def scout_find_by_id(id: int, payload, db):
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
                User.sub_detachment_id
            ).join(Rol).join(Church).\
                join(SubDetachment).\
                join(City).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).\
                filter(User.id == id).first()
            return {"data": res}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )

    async def create_scout(user,payload, db):
        try:
            new_user = User(**user)
            new_user.email = fake.email()
            new_user.sub_detachment_id = payload["sub_detachment_id"]
            new_user.church_id = payload["church_id"]
            new_user.rol_id = 13
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"data": user, "detail": "the data was saved successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )

    def create_test_scout(user, db):
        try:
            user = user.dict()
            new_user = User(
                first_name=user["first_name"],
                last_name=user["last_name"],
                identification=user["identification"],
                type_identification=user["type_identification"],
                birth_day=user["birth_day"],
                rh=user["rh"],
                direction=user["direction"],
                cell_phone=user["cell_phone"],
                grade=user["grade"],
                school_name=user["school_name"],
                eps_name=user["eps_name"],
                department_name=user["department_name"],
                location_name=user["location_name"],
                city_id=user["city_id"],
                church_id=user["church_id"],
                sub_detachment_id=user["sub_detachment_id"],
                rol_id=user["rol_id"],
                email=user["email"]
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {"data": user, "detail": "the data was saved successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )
    async def edit_scout(id: int, payload, data, db):
        try:
            result = db.query(User).filter(User.church_id == payload.get("church_id")).\
                filter(User.id == id).filter(User.rol_id == 13)
            if result.first() == None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id is not a valid")
            result.update(data)
            db.commit()
            return {"data": data, "detail": "the data was successfully updated"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )

    async def change_sub_detachment_scout(id: int, payload, db):
        try:
            data = db.query(User.sub_detachment_id, extract('year', func.age(User.birth_day)).label("age")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(User.id == id).filter(User.rol_id == 13)
            if data.first() == None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id is not a valid")

            result = db.query(User).filter(User.id == id).\
                filter(User.church_id == payload.get("church_id")).\
                filter(User.id == id).filter(User.rol_id == 13).first()
            if result == None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id is not a valid")
            data = data.first()
            result.sub_detachment_id = 2
            if data.age == 8:
                result.sub_detachment_id = 2
            if data.age == 11:
                result.sub_detachment_id = 3
            if data.age == 14:
                result.sub_detachment_id = 9
            db.commit()
            db.refresh(result)
            return {"data": result, "detail": "the data was successfully updated"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error:The id is not a valid"
            )
    