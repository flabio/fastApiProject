from fastapi import HTTPException,status
from apps.model.church_model import Church
from apps.utils import config_page


class ChurchRepository:
    
    async def all_churchs(name:str,page:int,limite:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(Church).count()
            page_offset= config_page.page_offset(page,limite)
            print("ddd->",limite)
            if limite==0:
                limite =5
            print(limite)
            page_total= config_page.page_total_cell(count_query,limite)
        
            res=db.query(Church).order_by(Church.id.desc())
            print(len(name))
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
                print("hola-> data",res)
            else:    
                res= res.filter(Church.name.ilike(search)).offset(page_offset).limit(limite).all()
            
            return {"data":res,"page_total":page_total }
            
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Error of query")
    
    async def find_church_by_id(id,db):
        try:
            return db.query(Church).filter(Church.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id is not a valid")
    
    async def create_church(church,db):
        try:
            new_church=Church(**church.dict())
            db.add(new_church)
            db.commit()
            db.refresh(new_church)
            return {"data":new_church,"msg":"the data was saved successfully"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e.args[0]}")
        
    async def update_church(id,church_update,db):
        try:
            
            church=db.query(Church).filter(Church.id==id)
            if not church.first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the rol is not a valid")
            church.update(church_update.dict(exclude_unset=True))
            db.commit()
            return {"data":church_update,"msg":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e.args[0]}")
    
    async def delete_church(id,db):
        try:
            church=db.query(Church).filter(Church.id==id)
            if not church.first():
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the rol is not a valid")
            church.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{e.args[0]}")

#private
            
            
    async def exist_name(name:str,db):
        res = db.query(Church).filter(Church.name == name).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="The name already exist")
    
    async def exist_email(email:str,db):
        res=db.query(Church).filter(Church.email == email).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="The email already exist")
