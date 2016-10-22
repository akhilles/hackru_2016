import numpy as np
import cv2

cap = cv2.VideoCapture("http://172.27.102.216:8080/video")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    

    # Display the resulting frame
    if ret==True:
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
