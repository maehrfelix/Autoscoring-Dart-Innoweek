"""
Kamera-Tester für Innoweek - Kameras 1-3 → Dartboard-Namen
WINDOWS UNICODE FIX - Keine Emojis!
"""

import cv2
import sys
import time
import os

# Windows Encoding Fix
if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

CAM_RANGE = [1, 2, 3]
REF_NAMES = {1: 'Dartboard_1.png', 2: 'Dartboard_2.png', 3: 'Dartboard_3.png'}

def capture_ref(cam_id):
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print(f"Erfasse Kamera {cam_id}...")
    time.sleep(2)
    
    ret, frame = cap.read()
    cap.release()
    
    if ret and frame is not None and frame.size > 0:
        filename = REF_NAMES[cam_id]
        cv2.imwrite(filename, frame)
        print(f"OK: {filename} ({frame.shape})")
        
        cv2.imshow(f'Ref {cam_id}', frame)
        print(f"Gespeichert: {filename}")
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        return True
    else:
        print(f"FEHLER Kamera {cam_id}: Schwarz")
        return False

def main():
    print("INNOWEEK REFERENZ-BILDER (Kam 1-3)")
    good = 0
    
    for cam_id in CAM_RANGE:
        if capture_ref(cam_id):
            good += 1
    
    print(f"\n{good}/3 Bilder OK!")
    if good == 3:
        print("Starte Autodarts.py!")
    else:
        print("Prufe USB/Privacy!")

if __name__ == "__main__":
    main()
