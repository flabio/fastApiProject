from fastapi import HTTPException,status
from apps.model.rol_model import Rol
from apps.utils import config_page


class RolRepository:
    
    async def all_rols(name:str,page:int,limite:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(Rol).count()
            page_offset= config_page.page_offset(page,limite)
            if limite==0:
                limite =20
                
            page_total= config_page.page_total_cell(count_query,limite)
            res=db.query(Rol).order_by(Rol.id.desc())
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else:    
                res= res.filter(Rol.name.ilike(search)).offset(page_offset).limit(limite).all()
            return {"data":res,"page_total":page_total }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    async def find_rol_by_id(id:int,db):
        try:
            return db.query(Rol).filter(Rol.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")
    
    async def create_rol(rol,db):
        try:
            new_rol=Rol(**rol.dict())
            db.add(new_rol)
            db.commit()
            db.refresh(new_rol)
            return {"data":new_rol,"detail":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
        
    async def update_rol(id:int,rol_update,db):
        try:
            rol=db.query(Rol).filter(Rol.id==id)
            if not rol.first() :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the rol is not a valid")
            rol.update(rol_update.dict(exclude_unset=True))
            db.commit()
            return {"data":rol_update,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The id of the rol is not a valid")
    
    async def delete_rol_by_id(id:int,db):
        try:
            rol=db.query(Rol).filter(Rol.id==id)
            if rol.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the rol is not a valid")
            rol.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")
    
    #private methods
    async def exist_name(name:str,db):
        rol = db.query(Rol).filter(Rol.name == name).first()
        if rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the name already exist")
    