import cv2
import os

import face_recognition

#codificar los rostros extraidos
imagesFacesPath="/home/isabella/Developers/workspace/python/ProyectoFastApi/sistema_asistencia/static/navegante_img_tmp"
facesEncodings=[]
facesNames=[]

for file_name in os.listdir(imagesFacesPath):
    image=cv2.imread(imagesFacesPath+"/"+file_name)
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    f_coding=face_recognition.face_encodings(image,known_face_locations=[(0,150,150,0)])[0]
    facesEncodings.append(f_coding)
    facesNames.append(file_name.split(".")[0])
# print(facesEncodings)
# print(facesNames)
imagesProfilePath="/home/isabella/Developers/workspace/python/ProyectoFastApi/sistema_asistencia/static/profile"

for file_name_profile in os.listdir(imagesProfilePath):
    #print(file_name_profile)
    image_p=cv2.imread(imagesProfilePath+"/"+file_name_profile)
    
    image_p=cv2.cvtColor(image_p,cv2.COLOR_BGR2RGB)
    
    a_f_coding=face_recognition.face_encodings(image_p,known_face_locations=[(0,150,150,0)])[0]
    result=face_recognition.compare_faces(facesEncodings,a_f_coding)
    print(result)
    if True in result:
        index=result.index(True)
        name=facesNames[index]
        color=(125,220,255)
        print(name)        
       
       

# faceClassif=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt2.xml")
# captura = cv2.VideoCapture(0)
# while (captura.isOpened()):
#     ret,frame=captura.read()
#     if ret == False:
#          break
#     frame = cv2.flip(frame,1)
#     orig=frame.copy()
#     faces=faceClassif.detectMultiScale(frame,1.1,5)
#     for (x,y,w,h) in faces:
#         face=orig[y:y+h,x:x+w]
#         face=cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
#         actual_face_encoding=face_recognition.face_encodings(face,known_face_locations=[(0,w,h,0)])[0]
        
#         result=face_recognition.compare_faces(facesEncodings,actual_face_encoding)
#         print(result)
#         if True in result:
#             index=result.index(True)
#             name=facesNames[index]
#             color=(125,220,255)
#             print(name)
#         else:
#             name="Desconocido"
#             color=(50,50,255)
#         cv2.rectangle(frame,(x,y+h),(x+w,y+h+38),color,-1)
#         cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255,0),2)
#         cv2.putText(frame,name,(x,y+h+25),2,1,(255,255,255),2,cv2.LINE_AA)
#     cv2.imshow("frame",frame)
#     k=cv2.waitKey(1) & 0xFF
#     if k == 27:
#         break

# #captura.release()
# cv2.destroyAllWindows()
    