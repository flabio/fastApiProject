import cv2
import numpy as np

faceClassif=cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

image=cv2.imread('234443434334.jpg')
imageAux=image.copy()
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
faces =faceClassif.detectMultiScale(gray,1.1,5 )
count=0
if faces is ():
    print("vacio")
# faces =faceClassif.detectMultiScale(gray,
#                                     scaleFactor=1.3,
#                                     minNeighbors=5,
#                                     minSize=(100,100),
#                                     maxSize=(200,200) )

for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    rostro=imageAux[y:y+h,x:x+w]
    #rostro=cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('rostro_{}.jpg'.format(count),rostro)
    count+=1
    cv2.imshow('rostro',rostro)
    cv2.imshow('image',image)
    #cv2.waitKey(0)
cv2.destroyAllWindows()