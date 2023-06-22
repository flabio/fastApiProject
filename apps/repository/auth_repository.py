from fastapi import HTTPException,status
from apps.model.user_model import User
from apps.model.rol_model import Rol
from apps.model.church_model import Church
from apps.model.sub_detachment_model import SubDetachment
from apps.model.detachment_model import Detachment
from sqlalchemy.sql import func
class AuthRepository:
    

       
    async def auth_login(username:str,db):
        try:
            user= db.query(
                    User.id,
                    User.first_name,
                    User.last_name,
                    User.rol_id,
                    User.username,
                    User.email,
                    User.image,
                    Rol.name.label("rol_name"),
                    User.is_active.label("user_active"),
                    User.church_id,
                    User.sub_detachment_id,
                    User.password,
                    Church.name.label("church_name"),  
                    SubDetachment.name.label("sub_detachment_name"),

                    func.CONCAT(Detachment.name," #",Detachment.numbers).label("detachment_name"),

                ).join(Rol).join(Church,Detachment).join(SubDetachment).filter(User.username==username).first()
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")

