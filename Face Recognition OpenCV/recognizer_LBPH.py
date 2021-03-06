import cv2
import numpy as np
import os 

recognizer_LBPH = cv2.face.LBPHFaceRecognizer_create()

recognizer_LBPH.read('trainer_LBPH.yml')

cascadePath = "/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Durgesh: id=1,  etc
names = ['None', 'Durgesh'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(1)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height


# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, img =cam.read()
   # img = cv2.flip(img, -1) # Flip vertically
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.3,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (144,0,0), 2)
        id, confidence_LBPH = recognizer_LBPH.predict(gray[y:y+h,x:x+w])
        
       
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence_LBPH < 70):
            id = names[id]
            confidence_LBPH = "  {0}%".format(round(100 - confidence_LBPH))
        else:
            id = "unknown"
            confidence_LBPH = "  {0}%".format(round(100 - confidence_LBPH))
        
        cv2.rectangle(img, (x,y), (x+w,y+30), (144,0,0), -1)
        cv2.putText(img, str(id), (x+2,y+23), font, 1, (255,255,255), 1)
        cv2.putText(img, str(confidence_LBPH), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

