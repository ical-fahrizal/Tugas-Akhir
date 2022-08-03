import numpy as np
import cv2
import database as db
import time
import os
from datetime import datetime
import threading as th

from flask import Flask, render_template, Response

app = Flask(__name__)

# @app.route('/')
# def index():
#     """Video streaming home page."""
#     return render_template('index.html')

#fungsi untuk mencari titik tengah bounding box
def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('1.mp4') #mengaktifkan kamera
cap.set(3, 260)
cap.set(4, 200)

fgbg = cv2.createBackgroundSubtractorMOG2()

detects = []

posL = 150
offset = 50

xy1 = (20, posL)
xy2 = (300, posL)

# filename = datetime.now().strftime('data logger-%Y-%m-%d.csv')
# file = open("data_log/{}".format(filename), "a")
# if os.stat("data_log/{}".format(filename)).st_size == 0:
#         file.write("Waktu,Pengunjung,Pelanggar Masker,Keterangan\n")


def jumlah_orang():
    print('hitung orang berjalan')
    prev_frame_time = 0
    new_frame_time = 0
    waktu = 0
    total = 0
    up = 0
    down = 0

    while(cap.isOpened()):
        ret, frame = cap.read()
        #cv2.resize(cap, (384, 288), interpolation = cv2.INTER_LINEAR)
        waktu += 0.1

        FPS = cap.get(cv2.CAP_PROP_FPS)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", gray)

        fgmask = fgbg.apply(gray)
        #cv2.imshow("fgmask", fgmask)

        retval, th = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        #cv2.imshow("th", th)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations = 2)
        #cv2.imshow("opening", opening)

        dilation = cv2.dilate(opening,kernel,iterations = 8)
        # #cv2.imshow("dilation", dilation)
        closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel, iterations = 10)
        #cv2.imshow("closing", closing)

        cv2.line(frame,xy1,xy2,(255,0,0),3)

        cv2.line(frame,(xy1[0],posL-offset),(xy2[0],posL-offset),(55, 255, 0),2)

        cv2.line(frame,(xy1[0],posL+offset),(xy2[0],posL+offset),(55, 255, 0),2)

        contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        #cntr = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
        #cv2.imshow('contour', cntr)
        i = 0
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)

            area = cv2.contourArea(cnt)
            
            if int(area) > 300 :
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

                    # if c > 0:
                    #     cv2.line(frame,detect[c-1],l,(0,0,255),1)
        new_frame_time = time.time()
        fps = 1/(new_frame_time-prev_frame_time)
        prev_frame_time = new_frame_time
 
        # converting the fps into integer
        fps = int(fps)

        cv2.putText(frame, "TOTAL: "+str(total), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)
        cv2.putText(frame, "MASUK: "+str(up), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),2)
        cv2.putText(frame, "KELUAR: "+str(down), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),2)
        cv2.putText(frame, "FPS: {}".format(FPS), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 255, 0),2)

        cv2.imshow("frame", frame)
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        #yield (b'--image\r\n'b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        #export data csv
        #now = datetime.now()
        # if (datetime.now().second % 5 == 0):
        #     file.write(str(now.strftime("%H:%M:%S"))+","+str(total)+","+str(up)+","+str(down)+"\n")
        #     file.flush()
        #     time.sleep(1)
        if waktu == 1.3:
            db.kirim_orang(total)
            waktu = 0
       
        time.sleep(0.1)
        # db.kirim_orang(total)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

jumlah_orang()

# @app.route('/video')
# def video():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(jumlah_orang(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', threaded=True)