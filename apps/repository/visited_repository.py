from fastapi import HTTPException, status
from apps.model.visit_model import Visit
from apps.model.user_model import User
from apps.model.sub_detachment_model import SubDetachment
from sqlalchemy import func, extract, or_
from datetime import datetime
from apps.utils import config_page


class VisitedRepository:

    async def all_visited(payload,q:str, page: int, limite: int, db):
        try:
            count_query = db.query(Visit).join(User).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).filter(User.rol_id == 13).count()
            page_offset = config_page.page_offset(page, limite)
            page_total = config_page.page_total_cell(count_query, limite)
            res = db.query(
                           Visit.id,
                           Visit.visit_date,
                           Visit.visit_hora,
                           Visit.visit_description,
                           Visit.visit_status,
                           Visit.user_id,
                           User.image,
                           func.CONCAT(User.first_name, "  ",
                                       User.last_name).label("full_name"),
                           ).\
                join(User).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(User.rol_id == 13)
             
            if len(q)>0:
                res=res.filter(Visit.visit_status==q)
                   
            res=res.order_by(Visit.id.desc()).\
            offset(page_offset).limit(limite).all()
            
            return {"data": res, "page_total": page_total}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.args[0]}")
    
    async def all_not_user_visited(payload,q:str, page: int, limite: int, db):
        try:
            data=[]
            search = "%{}%".format(q)
            res = db.query(Visit.user_id).\
                join(User).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(User.rol_id == 13).all()
            
            for item in res:
                data.append(item.user_id)

            if len(q) > 0:
                count_query = db.query(User).\
                filter(User.rol_id == 13).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(or_(User.first_name.ilike(search), User.last_name.ilike(search))).\
                filter(User.id.not_in(data)).count()
                
            else:
                count_query = db.query(User).\
                    filter(User.rol_id == 13).\
                    filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                    filter(User.church_id == payload.get("church_id")).filter(User.id.not_in(data)).count()
               
            
            page_offset = config_page.page_offset(page, limite)
            page_total = config_page.page_total_cell(count_query, limite)
            query_user = db.query(User.id,
                                  User.image,
                                  User.first_name,
                                  User.last_name,
                                  SubDetachment.image.label("sub_detachment_image"),
               ).join(SubDetachment).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(User.rol_id == 13).\
                filter(User.id.not_in(data))
            if len(q)>0:
                query_user = query_user.filter(or_(User.first_name.ilike(search), User.last_name.ilike(search)))
                  
            query_user = query_user.offset(page_offset).limit(limite).all()
            return {"data": query_user, "page_scout_total": page_total}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.args[0]}")

    async def all_visited_month(payload, db):
        try:
            result = db.query(Visit.id,
                              Visit.visit_date,
                              Visit.visit_hora,
                              Visit.visit_description,
                              Visit.visit_status,
                              User.cell_phone,
                              User.image,
                              func.CONCAT(User.first_name," ",User.last_name).label("full_name"),
                              ).\
                join(User).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(extract('month', (Visit.visit_date)) == datetime.now().month).\
                filter(Visit.visit_status=='Proceso').\
                all()
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.args[0]}")

    async def create_visited(data, db):
        try:
            new_data = Visit(**data.dict())
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data": new_data, "detail": "los datos se guardarón correctamente"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"{e}")

    async def update_visited(id: int, data, db):
        try:
            result = db.query(Visit).filter(Visit.id == id)
            if not result.first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="El id no es válido")
            result.update(data.dict(exclude_unset=True))
            db.commit()
            return {"data": data, "detail": "los datos se actualizarón correctamente"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"El id no es válido")

    async def delete_visited_by_id(id: int, db):
        try:
            result = db.query(Visit).filter(Visit.id == id)
            if result.first() is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="El id no es válido")
            result.delete(synchronize_session=False)
            db.commit()
            return {"data": True, "detail": "El registro fue eliminado con éxito"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="El id no es válido")
