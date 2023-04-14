from fastapi import APIRouter,Depends,status,HTTPException

from PIL import Image
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.scout_repository import ScoutRepository
from apps.repository.user import UserRepository
from apps.auth import check_comandant,oauth2_scheme,verify_token

from starlette.requests import Request
from apps.utils.profile_upload import update_upload_image_profile
import json
from typing import Optional
from faker import Faker
fake = Faker()
scout_router=APIRouter(
    prefix="/api/v1/scout",
    tags=["scout"]
)


@scout_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def alld_scouts(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 10,age:Optional[int]=0,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    result =await ScoutRepository.all_scouts(payload,q,page,limite,age,db)
    return result

@scout_router.get("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def scout_find_by(id: int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await ScoutRepository.scout_find_by(id,payload,db)

 
@scout_router.get("/scout_find_by_id/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def scout_find_by_id(id: int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await ScoutRepository.scout_find_by_id(id,payload,db)

@scout_router.get("/scout_change_to_sub_detachment/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def scout_change_to_sub_detachment(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await ScoutRepository.scout_change_to_sub_detachment(payload,db)


@scout_router.get("/all_scouts_age/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def all_scouts_age(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await ScoutRepository.all_scouts_age(payload,db)



@scout_router.post("/",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def create_scout(request:Request,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    form = await request.form()
    data = form.get("data").replace("'", "\"")
    validata_data = json.loads(data)
    validate_fields(validata_data)

    UserRepository.exist_identification(validata_data["identification"],db)
    if form!=None:
        if form['image']!="":
            filename= await update_upload_image_profile(form['image'])
            validata_data['image']=filename
    payload=verify_token(token)
    return await ScoutRepository.create_scout(validata_data,payload,db)
    
   
@scout_router.patch("/{id}",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def edit_scout(id:int,request:Request,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    form = await request.form()
    data = form.get("data").replace("'", "\"")
    validata_data = json.loads(data)
    validate_fields(validata_data)
    if form!=None:
        if form['image']!="":
            filename= await update_upload_image_profile(form['image'])
            validata_data['image']=filename
    payload=verify_token(token)
    return await ScoutRepository.edit_scout(id,payload,validata_data,db)
    

@scout_router.get("/change_sub_detachment_scout/{id}",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def change_sub_detachment_scout(id:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await ScoutRepository.change_sub_detachment_scout(id,payload,db)

#method private
def validate_fields(data):
    
    if len(data["first_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The first name is required")
    
    if len(data["last_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The last name is required")
    
    if len(data["identification"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The identification is required")
    
    if data["type_identification"]=="" or data["type_identification"]==None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The type identification is required")

    if len(data["direction"])==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if len(data["cell_phone"])==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if len(data["birth_day"])==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if len(data["rh"])==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if int(data["city_id"])<=0 :
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The city id is required")
    