from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import HTMLResponse
from apps.config.db import get_db
from sqlalchemy.orm  import Session 
from apps.repository.auth_repository import AuthRepository
from apps.auth import verify_password,create_access_token,verify_token

from apps.auth import oauth2_scheme
auth_router=APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)


@auth_router.post("/login",status_code=status.HTTP_200_OK)
async def login( form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    # new_user=user.dict()
    
    result= await AuthRepository.auth_login(form_data.username,db)
    
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated")
    if verify_password(form_data.password,result.password):
        token=create_access_token(result)
        data={
            'id':result.id,
            'full_name':result.first_name+" "+result.last_name,
            'image':result.image,
            'role':result.rol_name,
            'church_name': result.church_name,
            'detachment_name':result.detachment_name,
            'sub_detachment_name':result.sub_detachment_name
        }
        return {'user':data,'access_token':token,'token_type':'Bearer'}
    

@auth_router.get("/logout/{token}",status_code=status.HTTP_200_OK)
async def logout( token:str):
    # new_user=user.dict()
    
    verify_token(token)
    return {'user':None,'access_token':None,'token_type':''}
    

@auth_router.get("/verify/{token}", response_class=HTMLResponse)
async def login_user(token: str, db: Session = Depends(get_db)):
    payload = verify_token(token)
    username = payload.get("sub")
    db_user =await AuthRepository.auth_login(username,db)
 
    db.commit()
    return f"""
    <html>
        <head>
            <title>Bestätigung der Registrierung</title>
        </head>
        <body>
            <h2>Aktivierung von {username} erfolgreich!</h2>
            <a href="https://google.com">
                Zurück
            </a>
        </body>
    </html>
    """