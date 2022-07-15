import cv2
import database as db
import time
import csv
from flask import Flask, render_template, Response

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier('yahya.xml') #load model muka

cap = cv2.VideoCapture(0) #membuka webcam
cap.set(3, 240)
cap.set(4, 240)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def deteksi_masker():
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
        #cv2.imshow('img', frame0)
        test = cv2.imencode('.jpg', frame0)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + test + b'\r\n')
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        db.kirim_masker(pelanggar)
        time.sleep(0.2)

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(deteksi_masker(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)