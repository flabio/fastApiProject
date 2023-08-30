from fastapi import HTTPException, status
from apps.model.user_model import User
from apps.model.attendance_model import Attendace
from apps.model.church_model import Church
from apps.model.rol_model import Rol
from apps.model.sub_detachment_model import SubDetachment
from sqlalchemy import func, extract, or_,text,cast, Date
from datetime import datetime
import cv2
import os
import face_recognition
from apps.utils import config_page

class AttendaceRepository:

    async def all_attendace(id:int,payload,page:int,db):
        try:
            limite=5
            sub_detachment_id=payload["sub_detachment_id"]
            church_id=payload["church_id"]
            count_query=db.query(Attendace).join(User).\
                    filter(User.church_id==church_id).\
                    filter(User.sub_detachment_id == sub_detachment_id).\
                    filter(User.rol_id==13).filter(Attendace.user_id==id).count()
            page_offset= config_page.page_offset(page,limite)
           
            if limite==0:
                limite =5

            page_total= config_page.page_total_cell(count_query,limite)
            res = db.query(
                        Attendace.id,
                        Attendace.bible,
                        Attendace.offering,
                        Attendace.uniform,
                        Attendace.notebook,
                        Attendace.initial_letter,
                        Attendace.attendace_date
                ).join(User).filter(User.church_id==church_id).\
                    filter(User.sub_detachment_id == sub_detachment_id).\
                    filter(User.rol_id==13).filter(Attendace.user_id==id).order_by(Attendace.id.desc())
                    
            res= res.offset(page_offset).limit(limite).all()
            return {"data":res,"total_attendace":count_query,"page_total":page_total }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    async def create_attendace(data,db):
        try:
            new_data = Attendace(**data.dict())
            new_data.initial_letter= new_data.initial_letter.upper()
            db.add(new_data)
            db.commit()
            db.refresh(new_data)
            return {"data": new_data, "detail": "los datos se guardarón correctamente"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {e.args}"
            )
    async def delete_attendace_by_id(id:int,db):
        try:
            data=db.query(Attendace).filter(Attendace.id==id)
            if data.first() is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El id no es válido")
            data.delete(synchronize_session=False)
            db.commit()
            return {"data":True,"detail":"the record was successfully removed"}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The id of the rol is not a valid")
    
    async def all_scouts_by_call(payload, db):
        try:
            if payload.get("sub_detachment_id") == 1:
                age_begin = 0
                age_end=7
            if payload.get("sub_detachment_id") == 2:
                age_begin = 8
                age_end=10
            if payload.get("sub_detachment_id") == 3:
                age_begin = 11
                age_end=13
            if payload.get("sub_detachment_id") == 9:
                age_begin = 14
                age_end=17
            res = db.query(
                User.id,
                User.first_name,
                User.last_name,
                User.identification,
                User.type_identification,
                User.cell_phone,
                User.image,
                extract('year', func.age(User.birth_day)).label("age"),
                Church.name.label("church_name"),
                SubDetachment.name.label("sub_detachment_name"),
            ).join(Rol).join(Church).join(SubDetachment).join(Attendace).\
                filter(User.sub_detachment_id == payload.get("sub_detachment_id")).\
                filter(User.church_id == payload.get("church_id")).\
                filter(Rol.id == 13).filter(extract('day', func.age(cast(Attendace.created_at, Date)))>=15).\
                filter(extract('month', func.age(cast(Attendace.created_at, Date)))==0).\
                filter(extract('year', func.age(User.birth_day)).between(age_begin,age_end)).\
                order_by(User.ceated_at.desc()).all()
            return {"data": res}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error: {e}"
            )
    
    async def attendace_image_scout(payload,file, db):
        try:
            imagesPath=os.getenv("FILEPATH_TEMP")+"navegante_img_tmp/"
            count=0
            if not os.path.exists("static/navegante_img_tmp"):
                os.makedirs("static/navegante_img_tmp")
                print("new directory: faces")
            faceClassif=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt.xml")
            for imageName in os.listdir(imagesPath): 
                image=cv2.imread(imagesPath+"/"+imageName)
               
                faces=faceClassif.detectMultiScale(image,1.1,5)
                for(x,y,w,h) in faces:
                    #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                    face=image[y:y+h,x:x+w]
                    face=cv2.resize(face,(255,255))
                    cv2.imwrite("static/navegante_img_tmp/"+str(count)+".jpg",face)
                    count+=1
            imagesFacesPath=os.getenv("FILEPATH_DETACHMENT_TEMP")+"navegante_img_tmp"
            facesEncodings=[]
            facesNames=[]

            for file_name in os.listdir(imagesFacesPath):
                image_detachment=cv2.imread(imagesFacesPath+"/"+file_name)
                image_detachment=cv2.cvtColor(image_detachment,cv2.COLOR_BGR2RGB)
            
                f_coding=face_recognition.face_encodings(image_detachment,known_face_locations=[(0,150,150,0)])[0]
                facesEncodings.append(f_coding)
                facesNames.append(file_name.split(".")[0])
                
            
            
            
            scout = db.query(User).filter(User.sub_detachment_id == payload.get("sub_detachment_id")).all()
            generated_name_path="/home/isabella/Developers/workspace/python/ProyectoFastApi/sistema_asistencia/static/profile"
            for file_name_profile in os.listdir(generated_name_path):
               
                image_p=cv2.imread(generated_name_path+"/"+file_name_profile)
                
                image_p=cv2.cvtColor(image_p,cv2.COLOR_BGR2RGB)
                
                a_f_coding=face_recognition.face_encodings(image_p,known_face_locations=[(0,150,150,0)])[0]
                result=face_recognition.compare_faces(facesEncodings,a_f_coding)
            
                if True in result:
                    print(result)
                    index=result.index(True)
                    name=facesNames[index]
                    color=(125,220,255)
                    print(index)   
            # for data in scout:
               
                
            #     if data.image != None and data.image!="":
            #         name_img=data.image.split("profile")[1]
            #         print(name_img)
            #         # image_p=cv2.imread(generated_name)
            #         image_p=cv2.imread(generated_name_path+name_img)
            #         image_p=cv2.cvtColor(image_p,cv2.COLOR_BGR2RGB)
                  
            #         a_f_coding=face_recognition.face_encodings(image_p,known_face_locations=[(0,150,150,0)])[0]
            #         result=face_recognition.compare_faces(facesEncodings,a_f_coding)
            #         if True in result:
            #             print(result)
            #             index=result.index(True)
            #             name=facesNames[index]
            #             color=(125,220,255)
                       
            # db.query(User).filter(User.identification==121212).filter(Rol.id == 13).update(
            #     {User.image: file}, synchronize_session=False)
            # db.commit()
      
            return {"detail": "changed profile picture successfully"}
        except Exception as e:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="The format is not a valid"
            )
    #private
            
            
    async def exist_attendace(user_id:int,initial_letter:str,db):
        res = db.query(Attendace).\
            filter(Attendace.initial_letter == initial_letter.upper()).\
            filter(Attendace.user_id == user_id).first()
        if res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="Your assistance is already assigned")