from fastapi import APIRouter,Depends, File, UploadFile,status,HTTPException
from fastapi.staticfiles import StaticFiles
from PIL import Image
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.scout_repository import ScoutRepository
from apps.auth import check_comandant,oauth2_scheme,verify_token
from apps.schemas.user_schemas import ScoutSchema
from typing import List
from typing import Optional
from faker import Faker
fake = Faker()
scout_router=APIRouter(
    prefix="/api/v1/scout",
    tags=["scout"]
)


@scout_router.get("/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def alld_scouts(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 9,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    result =await ScoutRepository.all_scouts(payload.get("sub_detachment_id"),q,page,limite,db)
    return result

@scout_router.get("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def scout_find_by(id: int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    result =await ScoutRepository.scout_find_by(id,payload.get("sub_detachment_id"),db)
    return result

@scout_router.post("/",dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def create_scout(user:ScoutSchema,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    data_user=user.dict()
    user.email=fake.email()
    user.sub_detachment_id=payload["sub_detachment_id"]
    user.church_id=payload["church_id"]
 
    result= await ScoutRepository.create_user(user,db)
    return result
   




