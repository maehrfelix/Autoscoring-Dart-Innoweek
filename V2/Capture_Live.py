import cv2
import numpy as np
import time

# Kamera-Indizes (0=laptop, 1=erste USB, 2=zweite USB)
cam1_id, cam2_id = 1, 2  # Anpassen!

cap1 = cv2.VideoCapture(cam1_id, cv2.CAP_DSHOW)
cap2 = cv2.VideoCapture(cam2_id, cv2.CAP_DSHOW)

cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

time.sleep(2)  # Init

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    
    if ret1 and ret2:
        # Nebeneinander kleben (hconcat)
        combined = np.hstack((frame1, frame2))
        # Oder untereinander: np.vstack((frame1, frame2))
        
        cv2.imshow('Dual Kam: 1 | 2 (q=quit)', combined)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
