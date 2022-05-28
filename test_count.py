import cv2
import numpy as np
from time import sleep

width_min=80
height_min=80 

# posL = 150
# offset = 10
offset=5
pos_line=150 

xy1 = (20, pos_line)
xy2 = (300, pos_line)

delay= 600
detec = []
car= 0

def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('1.mp4')
subtraction = cv2.createBackgroundSubtractorMOG2()

while True:
    ret , frame1 = cap.read()
    time = float(1/delay)
    sleep(time) 
    
    grey = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(3,3),5)
    
    img_sub = subtraction.apply(blur)
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    expand = cv2.morphologyEx (dilat, cv2. MORPH_CLOSE , kernel)
    expand = cv2.morphologyEx (expand, cv2. MORPH_CLOSE , kernel)
    contour,h=cv2.findContours(expand,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.line(frame1, (25, pos_line), (1200, pos_line), (255,127,0), 3) 
    for(i,c) in enumerate(contour):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_outline = (w >= width_min) and (h >= height_min)
        if not validate_outline:
            continue

        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)   
        
        center = pega_centro(x, y, w, h)
        detec.append(center)
        cv2.circle(frame1, center, 4, (0, 0,255), -1)

        for detects in detec:
            for(x,y) in enumerate(detec):
                if detec[x-1][1] < pos_line and y[1] > pos_line :
                    detec.clear()
                    car+=1
                    cv2.line(frame1,xy1,xy2,(0,255,0),5)
                    print('tambah')
                    continue

                if detec[x-1][1] > pos_line and y[1] < pos_line:
                    detec.clear()
                    car-=1
                    cv2.line(frame1,xy1,xy2,(0,0,255),5)
                    print('kurang')
                    continue
        # for (x,y) in detec:
        #     if y<(pos_line+offset) and y>(pos_line-offset):
        #         detec.clear()
        #         car+=1
        #         cv2.line(frame1, (25, pos_line), (1200, pos_line), (0,127,255), 3)  
        #         print('tambah')
        #         continue
        #     if y>(pos_line+offset) and y<(pos_line-offset):
        #         detec.clear()
        #         car-=1
        #         cv2.line(frame1, (25, pos_line), (1200, pos_line), (0,127,255), 3) 
        #         print('kurang') 
        #         continue
    cv2.putText(frame1, "Kendaraan Lewat : "+str(car), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),2)
    cv2.imshow("Detector",expand)
    cv2.imshow("Video Original" , frame1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()