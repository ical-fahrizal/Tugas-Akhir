import cv2
import database as db

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #load model muka

cap = cv2.VideoCapture(0) #membuka webcam
pelanggar = 0

def scale_vidio():
    cap.set(3, 384)
    cap.set(4, 400)
    # cap.set(3, 384)
    # cap.set(4, 288)

scale_vidio()

def deteksi_masker():
    global pelanggar
    print('deteksi wajah berjalan')
    while True:
        ret0, frame0 = cap.read()
        pelanggar = 0

        gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y , w ,h) in faces:
            cv2.rectangle(frame0, (x,y), (x+w, y+h), (3, 252, 169), 2)
            pelanggar += 1
       
        cv2.putText(frame0, 
                    'Pelanggar masker =  ' + str(pelanggar), 
                    (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                    (0, 255, 255), 
                    1, 
                    cv2.LINE_4)
        db.kirim_masker(pelanggar)
        cv2.imshow('img', frame0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
deteksi_masker()
cap.release()
cv2.destroyAllWindows()
    
