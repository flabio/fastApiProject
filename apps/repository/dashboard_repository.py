from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.parentesco_model import Parentesco,Scoutkindred 
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.city_model import City
from apps.model.sub_detachment_model import SubDetachment
from apps.utils import config_page
from sqlalchemy import func
from faker import Faker
fake = Faker()
class DashboardRepository:
    async def counts_scouts(db):
        try:
            query_count=db.query(User).join(Rol).join(Church).join(SubDetachment).filter(Rol.id==13)
            navegantes_count=query_count.filter(User.sub_detachment_id == 1).count()
            pioneros_count=query_count.filter(User.sub_detachment_id == 2).count()
            seguidores_count=query_count.filter(User.sub_detachment_id == 3).count()
            exporadores_count=query_count.filter(User.sub_detachment_id == 9).count()
            return {
                    "navegantes_count":navegantes_count,
                    "pioneros_count":pioneros_count,
                    "seguidores_count":seguidores_count,
                    "exporadores_count":exporadores_count,
                    
                    }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    