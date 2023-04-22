from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.parentesco_model import Parentesco, Scoutkindred
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.city_model import City
from apps.model.sub_detachment_model import SubDetachment
from apps.model.detachment_model import Detachment
from sqlalchemy import func, extract
from faker import Faker
fake = Faker()


class DashboardRepository:
    
    async def counts_scouts(church_id,year, db):
        try:

            query_count = db.query(User).join(Rol).join(
                Church).join(SubDetachment).filter(Rol.id == 13)
            if church_id > 0:
                query_count = query_count.filter(User.church_id == church_id)
            if year>0:
                 query_count = query_count.filter(extract('year',User.ceated_at) == year)
            if church_id > 0 and year > 0:
                query_count = query_count.filter(User.church_id == church_id).filter(extract('year',User.ceated_at) == year)
            
            navegantes_count = query_count.filter(
                User.sub_detachment_id == 1).count()
            pioneros_count = query_count.filter(
                User.sub_detachment_id == 2).count()
            seguidores_count = query_count.filter(
                User.sub_detachment_id == 3).count()
            exporadores_count = query_count.filter(
                User.sub_detachment_id == 9).count()
            return {
                "navegantes_count": navegantes_count,
                "pioneros_count": pioneros_count,
                "seguidores_count": seguidores_count,
                "exporadores_count": exporadores_count,
                 }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
            
    async def chart_by_year_scouts(church_id,year, db):
        try:
            query = db.query(func.count( User.id).label("count"),extract('year',User.ceated_at).label("year")).join(Rol).join(
                Church).join(SubDetachment).filter(Rol.id == 13)
            if church_id > 0:
                query = query.filter(User.church_id == church_id)
            return query.group_by(extract('year',User.ceated_at)).limit(10).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
            
    async def chart_church__scouts(church_id,year, db):
        try:
            query = db.query(func.count( User.church_id).label("count"),Detachment.name.label("name"),Detachment.numbers).join(Rol).join(
                Church,Detachment).join(SubDetachment).filter(Rol.id == 13)
            if year>0:
                 query = query.filter(extract('year',User.ceated_at) == year)
            return  query.group_by(Detachment.name,Detachment.numbers).all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )