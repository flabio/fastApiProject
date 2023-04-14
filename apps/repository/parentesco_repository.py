from fastapi import HTTPException, status
from apps.model.parentesco_model import Parentesco,Scoutkindred
from apps.utils import config_page


class ParentescoRepository:

    async def all_parentesco(payload,name:str,page:int,limite:int,db):
        try:
            search = "%{}%".format(name)
            count_query=db.query(Parentesco).filter(Parentesco.church_id==payload.get("church_id")).count()
            page_offset= config_page.page_offset(page,limite)
        
            if limite==0:
                limite =10
        
            page_total= config_page.page_total_cell(count_query,limite)
            res = db.query(
                    Parentesco.id,
                    Parentesco.first_name,
                    Parentesco.last_name,
                    Parentesco.identification,
                    Parentesco.type_parentesco,
                    Parentesco.civil_status,
                    Parentesco.direction,
                    Parentesco.cell_phone,
                    Parentesco.is_active,
                ).filter(Parentesco.church_id==payload.get("church_id")).order_by(Parentesco.id.desc())
            if name==None:
                res= res.offset(page_offset).limit(limite).all()
            else:    
                res= res.filter(Parentesco.first_name.ilike(search) ).offset(page_offset).limit(limite).all()
            return {"data":res,"page_total":page_total }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
   
    async def find_parentesco_by_id(id: int,payload, db):
        try:
            result = db.query(
               Parentesco.id,
                    Parentesco.first_name,
                    Parentesco.last_name,
                    Parentesco.identification,
                    Parentesco.type_parentesco,
                    Parentesco.civil_status,
                    Parentesco.direction,
                    Parentesco.cell_phone,
                    Parentesco.is_active,
                ).filter(Parentesco.id == id).filter(Parentesco.church_id==payload.get("church_id")).first()
            return {"parentesco":result}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e.args[0]}")

    async def create_parentesco(data,payload, db):
        try:
            new_data = Parentesco(**data.dict())
            new_data.church_id=payload.get("church_id")
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data": new_data, "detail": "the data was saved successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            )

    async def update_parentesco(id: int, data, db):
        try:
            result = db.query(Parentesco).filter(Parentesco.id == id)
            if not result.first():
                return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the kindred is not a valid")
            result.update(data.dict(exclude_unset=True))
            db.commit()
            return {"data":data,"detail":"the data was successfully updated"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the kindred is not a valid")

    async def delete_parentesco_by_id(id: int, db):
        try:
            result = db.query(Parentesco).filter(Parentesco.id == id)
            if result.first() is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the kindred is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return {"detail": "the record was successfully deleted."}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The id of the kindred is not a valid")
    
    # add scout a kindred
    async def add_scout_kindred(data, db):
        try:
            new_data = Scoutkindred(**data.dict())
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data": new_data, "detail": "the kindred was add successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args[0]}"
            ) 
    async def delete_scout_kindred_by_id(id: int, db):
        try:
            result = db.query(Scoutkindred).filter(Scoutkindred.id == id)
            if result.first() is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the kindred is not a valid")
            result.delete(synchronize_session=False)
            db.commit()
            return {"detail": "the record was successfully deleted."}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="The id of the kindred is not a valid")
    # private

    async def exist_id(id: int,payload, db):
        result = db.query(Parentesco).filter(Parentesco.id == id).filter(Parentesco.church_id==payload.get("church_id")).first()
   
        if result == None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The id of the parentesco is not a valid")
    
    def exist_identification(identification:str,payload, db):
        result = db.query(Parentesco).filter(
            Parentesco.identification == identification).filter(Parentesco.church_id==payload.get("church_id")).first()
        if result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="identification already exist")
    async def exist_kindred(scout_id: int,kindred_id:int, db):
        result = db.query(Scoutkindred).filter(Scoutkindred.scout_id == scout_id).filter(Scoutkindred.parentesco_id == kindred_id).first()
     
        if result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="the kindred you selected already has it associated")
    