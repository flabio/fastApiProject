from fastapi import HTTPException,status
from pathlib import Path
from dotenv import load_dotenv
import os
import secrets
env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

def  remove_exist(user):
    
    if user[0]!=None:
            img=user[0].split("/")[5]
            remove_file = Path(os.getenv('FILEPATH')+img)
            remove_file.unlink(missing_ok=True)
            
async def update_upload_image_profile(file):
   
    token_name=secrets.token_hex(10)
    filename=file.filename
    
    extension=filename.split(".")[1]
    
    if extension not in ["png", "jpg", "jpeg","webp"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The format is not a valid")
    
    generated_name=os.getenv('FILEPATH')+token_name+"."+extension
    file_content=await file.read()
    with open(generated_name,'wb+') as f:
        f.write(file_content)
        f.close()
    return os.getenv('PATH_SERVER')+generated_name[1:]

async def update_upload_image_sub_detachment(file):
   
    token_name=secrets.token_hex(10)
    filename=file.filename
    
    extension=filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg","webp"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The format is not a valid")
    
    generated_name=os.getenv('FILEPATH_DETACHMENT')+token_name+"."+extension
    file_content=await file.read()
    with open(generated_name,'wb+') as f:
        f.write(file_content)
        f.close()
    return os.getenv('PATH_SERVER')+generated_name[1:]