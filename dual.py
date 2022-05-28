import cv2

cap = cv2.VideoCapture(0) #membuka webcam
cap2 = cv2.VideoCapture(1) #membuka webcam

while True:
    ret0, frame0 = cap.read()
    ret1, frame1 = cap2.read()

    if(ret0):
        cv2.imshow('cam 0', ret0)
    if(ret1):
        cv2.imshow('cam 1', ret1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap2.release()
cv2.destroyAllWindows()