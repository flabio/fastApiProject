from fastapi import APIRouter,Depends,status

from  apps.schemas.city_schemas import CitySchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.model.city_model import City
from apps.repository.city_repository import CityRepository
from apps.auth import check_admin

city_router=APIRouter(
    prefix="/api/v1/cities",
    tags=["cities"]
)


@city_router.get("/",status_code=status.HTTP_200_OK)
async def get_cities(db:Session=Depends(get_db)):
    return await CityRepository.all_citys(db)
 
@city_router.post("/", dependencies=[Depends(check_admin)],status_code=status.HTTP_201_CREATED)
async def create_city(data:CitySchema,db:Session=Depends(get_db)):
    new_data =data.dict()
    await CityRepository.exist_name(new_data["name"],db)
    await CityRepository.exist_postal_code(new_data["postal_code"],db)
    result=await  CityRepository.create_city(data,db)
    return result


@city_router.patch("/{id}", dependencies=[Depends(check_admin)],status_code=status.HTTP_201_CREATED)
async def update_city(id:int,city:CitySchema,db:Session=Depends(get_db)):
    result=await  CityRepository.update_city(id,city,db)
    return result

@city_router.delete("/{id}", dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def delete_city(id:int,db:Session=Depends(get_db)):
    return await  CityRepository.delete_city_by_id(id,db)
    