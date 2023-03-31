from fastapi import HTTPException,status
from apps.model.user_model import User
from apps.model.rol_model import Rol
from apps.model.church_model import Church

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
                   User.password
                ).filter(User.username==username).where(User.rol_id==Rol.id).first()
            return user
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")

