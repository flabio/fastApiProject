from fastapi import APIRouter,Depends, File, UploadFile,status,HTTPException
from fastapi.staticfiles import StaticFiles
from PIL import Image
from  apps.schemas.user_schemas import UserSchema,UserChangePasswordSchema
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.user import UserRepository
from apps.auth import check_admin,check_comandant,verify_token,oauth2_scheme
from typing import List
from apps.utils.profile_upload import update_upload_image_profile
from typing import Optional
router=APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)


@router.get("/", dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def read_users(q: Optional[str] = None,page: Optional[int] = 1,limite: Optional[int] = 10,rol: Optional[int] = 0,db:Session=Depends(get_db)):
    return await UserRepository.all_users(q,page,limite,rol,db)
   
@router.get("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def find_user_by_id(id:int,db:Session=Depends(get_db)):
    await UserRepository.exist_id(id,db)
    result=await UserRepository.find_user_by_id(id,db)
    return {"data":result}


@router.get("/birth_day_commenders/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def birth_day_commenders(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await UserRepository.birth_day_commenders(payload,db)
 
@router.get("/birth_day_scouts/", dependencies=[Depends(check_comandant)],status_code=status.HTTP_200_OK)
async def birth_day_scouts(db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload=verify_token(token)
    return await UserRepository.birth_day_scouts(payload,db)

 
@router.put("/change_image_profile/{id}",status_code=status.HTTP_201_CREATED)
async def change_imagen_profile_user( id:int,thumbnail: UploadFile = File(...),db:Session=Depends(get_db)):
    filename= await update_upload_image_profile(thumbnail)
    return await UserRepository.update_by_image_user(id,filename,db)


@router.post("/", dependencies=[Depends(check_admin)],status_code=status.HTTP_201_CREATED)
async def create_user( user:UserSchema,db:Session=Depends(get_db)):
    new_user=user.dict()
    _validates_fields(new_user)
    if len(new_user["password"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The password is required")

    # if len(new_user["password"])>=6 and len(new_user["password"])<=14:
    #     raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,detail="the password must be greater than 6 and less than 14 characters")
    UserRepository.exist_identification(new_user["identification"],db)
  
    UserRepository.exist_email(new_user["email"],db)
    return await UserRepository.create_user(user,db)
 

@router.patch("/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_201_CREATED)
async def update_user(id:int, user_update:UserSchema,db:Session=Depends(get_db)):
    new_user=user_update.dict()
    _validates_fields(new_user)
    return await UserRepository.update_user(id,user_update,db)
   


@router.patch("/change_password/{id}", dependencies=[Depends(check_comandant)],status_code=status.HTTP_201_CREATED)
async def update_password(id:int, user_password_update:UserChangePasswordSchema,db:Session=Depends(get_db)):
    if len(user_password_update.password)<=7:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="minimo es de 8 caracteres")
    
    if user_password_update.password!=user_password_update.comfirm_password:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña son diferente.")
    return await UserRepository.update_password_user(id,user_password_update,db)
    

@router.delete("/{id}", dependencies=[Depends(check_admin)],status_code=status.HTTP_200_OK)
async def delete_user_by_id(id:int,db:Session=Depends(get_db)):
    
    user=await UserRepository.delete_user_by_id(id,db)
    if user:
        return {"response": "Se elimino existosamente"}
    return {"response": "No se puede eliminar el id del user"}

def _validates_fields(new_user):
    
    if len(new_user["first_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The first name is required")
    
    if len(new_user["last_name"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The last name is required")
    
    if len(new_user["identification"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The identification is required")
    
    if new_user["type_identification"]=="" or new_user["type_identification"]==None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The type identification is required")
    
    if len(new_user["expedition_date"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The expedition date is required")
    
    if len(new_user["birth_day"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The birth day is required")
    
    if len(new_user["birth_place"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The birth place is required")
    
    if len(new_user["gender"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The gender is required")
    if len(new_user["rh"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The rh is required")
    
    if len(new_user["direction"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The direction is required")
    
    if len(new_user["cell_phone"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The cell phone is required")
    
    if len(new_user["civil_status"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The civil status is required")
    
    if new_user["rol_id"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The rol_id is required")
    if new_user["church_id"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The church id is required")
    
    if new_user["city_id"]<=0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The city id is required")
    if len(new_user["email"])==0:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,detail="The email is required")
