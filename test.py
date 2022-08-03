import numpy as np
import cv2
import database as db
import time
import os
import time 
from time import sleep
from datetime import datetime
from flask import Flask, render_template, Response

app = Flask(__name__)

cap_orang = cv2.VideoCapture(0)
cap_orang.set(3, 240)
cap_orang.set(4, 240)
cap_masker = cv2.VideoCapture(1)
cap_masker.set(3, 240)
cap_masker.set(4, 240)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #load model muka

fgbg = cv2.createBackgroundSubtractorMOG2()

detects = []

posL = 150
offset = 50

xy1 = (20, posL)
xy2 = (300, posL)

pelanggar = 0
total = 0
up = 0
down = 0

print('hitung orang berjalan')
def citra():
    global pelanggar
    global total
    global up
    global down
    while True:
        ret, frame0 = cap_masker.read()
        ret1, frame = cap_orang.read()
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
        # cv2.imshow('img', frame0)

        # #cv2.resize(cap, (384, 288), interpolation = cv2.INTER_LINEAR)

        gray_orang = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray", gray_orang)

        fgmask = fgbg.apply(gray_orang)
        # cv2.imshow("fgmask", fgmask)

        retval, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        # cv2.imshow("th", th)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations = 2)
        # cv2.imshow("opening", opening)

        dilation = cv2.dilate(opening,kernel,iterations = 8)
        # cv2.imshow("dilation", dilation)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations = 8)
        # cv2.imshow("closing", closing)

        cv2.line(frame,xy1,xy2,(255,0,0),3)

        # cv2.line(frame,(xy1[0],posL-offset),(xy2[0],posL-offset),(255,255,0),2)

        # cv2.line(frame,(xy1[0],posL+offset),(xy2[0],posL+offset),(255,255,0),2)

        contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)

            area = cv2.contourArea(cnt)
            
            if int(area) > 3000 :
                centro = center(x, y, w, h)

                # cv2.putText(frame, str(i), (x+5, y+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)
                cv2.circle(frame, centro, 4, (0, 0,255), -1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                if len(detects) <= i:
                    detects.append([])
                if centro[1]> posL-offset and centro[1] < posL+offset:
                    detects[i].append(centro)
                else:
                    detects[i].clear()
                i += 1

        if i == 0:
            detects.clear()

        i = 0

        if len(contours) == 0:
            detects.clear()

        else:

            for detect in detects:
                for (c,l) in enumerate(detect):
                    if detect[c-1][1] < posL and l[1] > posL :
                        detect.clear()
                        up+=1
                        total+=1
                        cv2.line(frame,xy1,xy2,(0,255,0),5)
                        continue

                    if detect[c-1][1] > posL and l[1] < posL:
                        detect.clear()
                        down+=1
                        total-=1
                        cv2.line(frame,xy1,xy2,(0,0,255),5)
                        continue

                    if c > 0:
                        cv2.line(frame,detect[c-1],l,(0,0,255),1)

        cv2.putText(frame, "TOTAL: "+str(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)
        cv2.putText(frame, "MASUK: "+str(up), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),2)
        cv2.putText(frame, "KELUAR: "+str(down), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),2)

        # cv2.imshow("frame", frame)
        both = np.column_stack((frame,frame0))
        #both = np.concatenate((frame, frame0), axis=0)
        #cv2.imshow('join', both)
        vidio = cv2.imencode('.jpg', both)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + vidio + b'\r\n')
        #db.kirim_orang(total)
        #db.kirim_masker(pelanggar)
        time.sleep(.2)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(citra(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
# cap_orang.release()
# cap_masker.release()
cv2.destroyAllWindows()