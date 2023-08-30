import cv2
import os

imagesPath="/home/isabella/Developers/workspace/python/ProyectoFastApi/sistema_asistencia/temp_img/"
if not os.path.exists("static/faces"):
    os.makedirs("static/faces")
    print("new directory: faces")
count=0
#Detector facial
faceClassif=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_alt.xml")
for imageName in os.listdir(imagesPath): 
   
    image=cv2.imread(imagesPath+"/"+imageName)
    faces=faceClassif.detectMultiScale(image,1.1,5)
    for(x,y,w,h) in faces:
        #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        face=image[y:y+h,x:x+w]
        face=cv2.resize(face,(155,155))
        cv2.imwrite("static/faces/"+str(count)+".jpg",face)
        count+=1
        # cv2.imshow("Face",face)
        # cv2.waitKey(0)
    # cv2.imshow("Image",image)
    # cv2.waitKey(0)
cv2.destroyAllWindows()