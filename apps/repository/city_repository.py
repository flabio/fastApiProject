from fastapi import HTTPException,status
from apps.model.city_model import City


class CityRepository:
    
    async def all_citys(db):
        try:
            return db.query(City).all()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
    
    async def create_city(city,db):
        try:
            new_city=city(**city.dict())
            db.add(new_city)
            db.commit()
            db.refresh(new_city)
            return new_city
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{e.args[0]}")
        
    async def update_city(id:int,city_update,db):
        try:
            city=db.query(City).filter(City.id==id)
            if not city.first() :
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The id of the city is not a valid")
            city.update(city_update.dict(exclude_unset=True))
            db.commit()
            return city_update
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The id of the city is not a valid")
    
    async def delete_city_by_id(id:int,db):
        try:
            city=db.query(City).filter(City.id==id)
            if city.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The id of the city is not a valid")
            city.delete(synchronize_session=False)
            db.commit()
            return True
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the city is not a valid")
    
    #private methods
    async def exist_name(name:str,db):
        city = db.query(City).filter(City.name == name).first()
        if city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the name already exist")
    
    async def exist_postal_code(postal_code:str,db):
        city = db.query(City).filter(City.postal_code == postal_code).first()
        if city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="the postal_code already exist")