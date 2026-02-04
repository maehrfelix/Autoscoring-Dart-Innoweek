"""
FIXED DART-SCORING v2.0 - Statische Erkennung + perfekte Overlays
Darts bleiben sichtbar + volle Scheibe + gleiche Größe
"""

import cv2
import numpy as np
import time
import os
import sys

if os.name == 'nt':
    sys.stdout.reconfigure(encoding='utf-8')

class DartScorer:
    def __init__(self):
        self.cam_ids = [1,2,3]
        self.cam_names = ['Links', 'Rechts', 'Mitte']
        self.vidcaps = [None]*3
        self.prev_frames = [None]*3
        self.dart_history = [[], [], []] 
        self.board_centers = [(320,240)]*3
        
        self.scores = [20,1,18,4,13,6,10,15,2,17,3,19,7,16,8,11,14,9,12,5]
    
    def init_cameras(self):
        for i, cam_id in enumerate(self.cam_ids):
            self.vidcaps[i] = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
            self.vidcaps[i].set(3, 640)
            self.vidcaps[i].set(4, 480)
            time.sleep(1)
            ret, frame = self.vidcaps[i].read()
            if ret:
                self.prev_frames[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                print(f"OK {self.cam_names[i]}")
    
    def detect_static_darts(self, cam_id):
        ret, frame = self.vidcaps[cam_id].read()
        if not ret: return frame, []
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        
        # Kreise finden
        mask = cv2.inRange(hsv, np.array([10,100,100]), np.array([30,255,255]))
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=20, minRadius=8, maxRadius=25)
        
        darts = []
        if circles is not None:
            circles = np.round(circles[0,:]).astype("int")
            for (x,y,r) in circles:
                # Score berechnen (genau)
                dx, dy = x - 320, y - 240
                angle = int((np.arctan2(dy, dx) + np.pi) * 10 / np.pi) % 20
                dist = np.sqrt(dx**2 + dy**2)
                
                score = self.scores[angle]
                if dist < 15: score = 50
                elif dist < 30: score = 25
                elif dist > 280: score = 0
                else: 
                    if dist > 250: score *= 2  # Double
                
                darts.append({'x':x, 'y':y, 'r':r, 'score':score})
                
                # Zeichnen
                cv2.circle(frame, (x,y), r, (0,255,255), 2)
                cv2.circle(frame, (x,y), 2, (0,0,255), -1)
                cv2.putText(frame, f"{score}", (x-20,y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        
        self.dart_history[cam_id].extend(darts)
        self.dart_history[cam_id] = self.dart_history[cam_id][-5:]  # Letzte 5
        
        return frame, darts
    
    def draw_full_board(self, frame, cam_id):
        """PERFEKTES Board-Overlay - Genau positioniert"""
        h, w = frame.shape[:2]
        cx, cy = 320, 240  # Fix-Center
        
        # Bullseye
        cv2.circle(frame, (cx,cy), 12, (0,0,255), 3)
        cv2.circle(frame, (cx,cy), 25, (255,165,0), 2)  # 25 Ring
        
        # Wires + Numbers
        for i in range(20):
            angle = i * 18
            rad = np.radians(angle)
            ex = int(cx + 220 * np.cos(rad))
            ey = int(cy + 220 * np.sin(rad))
            
            # Wire
            cv2.line(frame, (cx,cy), (ex,ey), (100,100,100), 2)
            
            # Number
            num_x = int(cx + 240 * np.cos(rad))
            num_y = int(cy + 240 * np.sin(rad))
            cv2.putText(frame, str(self.scores[i]), (num_x-10, num_y+5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        
        # Rings
        cv2.circle(frame, (cx,cy), 150, (0,255,255), 2)  # Single-Double
        cv2.circle(frame, (cx,cy), 280, (255,0,255), 2)  # Outer
        
        # Historische Darts
        for dart in self.dart_history[cam_id]:
            alpha = 0.7 ** (self.dart_history[cam_id].index(dart)+1)
            cv2.circle(frame, (int(dart['x']), int(dart['y'])), dart['r'], (0,255,0), 2)
        
        # Header
        cv2.rectangle(frame, (0,0), (220,90), (0,0,0), -1)
        cv2.putText(frame, self.cam_names[cam_id], (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, f"Aktuell: {len(self.dart_history[cam_id])}", (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
        
        return frame
    
    def run(self):
        self.init_cameras()
        print("LIVE DART-SCORING v2 - q=Quit, s=Shot")
        
        while True:
            frames = []
            
            for i in range(3):
                frame, darts = self.detect_static_darts(i)
                frame = self.draw_full_board(frame, i)
                frames.append(frame)
            
            # Combined - GLEICHE GRÖSSE!
            h1 = np.hstack((frames[0], frames[1]))
            h2 = np.hstack((frames[2], np.zeros((480,640,3), dtype=np.uint8)))
            combined = np.vstack((h1, h2))
            
            # Total Score (letzte 3 Darts pro Kam)
            total = sum(len(h) for h in self.dart_history)
            cv2.putText(combined, f"TOTAL DARTS: {total}", (20,50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
            
            cv2.imshow('3-KAM DART-SCORING v2.0', combined)
            
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'): break
            if k == ord('s'): 
                cv2.imwrite('dart_scoring_v2.png', combined)
                print("Screenshot!")
        
        for cap in self.vidcaps: cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    scorer = DartScorer()
    scorer.run()
