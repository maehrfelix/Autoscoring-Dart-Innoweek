import cv2
import numpy as np
import time
import os
import math

# Windows Fix
if os.name == 'nt':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

class InnoweekDartScorer:
    def __init__(self):
        self.cam_ids = [1,2,3]  # Eure Kameras
        self.vidcaps = []
        self.board_circles = [(320,240,200)] * 3  # Start-Schätzung
        self.dart_scores = [0, 0, 0]  # Pro Kamera
        self.total_score = 0
        
    def init_cameras(self):
        self.vidcaps = []
        for cam_id in self.cam_ids:
            cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
            cap.set(3, 640)
            cap.set(4, 480)
            time.sleep(0.5)
            self.vidcaps.append(cap)
        print("3 Kameras bereit!")

    def find_board_circle(self, frame):
        """Scheibe finden - Robust für euer Setup"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (9,9), 2)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # HoughCircles - angepasst an euer Bild
        circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1.3, 100,
                                  param1=80, param2=25,
                                  minRadius=120, maxRadius=250)
        
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            # Größten Kreis nehmen
            best = max(circles, key=lambda c: c[2])
            return best
        return (320, 240, 180)  # Fallback

    def detect_darts(self, frame, circle):
        """Dart-Erkennung - Diff + Color"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Dart-Flights (gelb/orange)
        lower_dart = np.array([15, 80, 80])
        upper_dart = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, lower_dart, upper_dart)
        
        # Kleine Kreise (Dart-Spitzen)
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20,
                                  param1=30, param2=15,
                                  minRadius=5, maxRadius=20)
        
        darts = []
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                # Innerhalb Scheibe?
                cx, cy, cr = circle
                if math.hypot(x-cx, y-cy) < cr*0.95:
                    # Score berechnen
                    dx = x - cx
                    dy = y - cy
                    angle = int((math.atan2(dy, dx) + math.pi) * 10 / math.pi) % 20
                    dist = math.hypot(dx, dy)
                    
                    score = self.scores[angle]
                    if dist < 20:
                        score = 50
                    elif dist < 40:
                        score = 25
                    elif dist > cr * 0.9:
                        score *= 2  # Double
                    
                    darts.append({'x':x, 'y':y, 'score':score})
        
        return darts

    def draw_board_overlay(self, frame, circle):
        """Vollständiges Overlay"""
        cx, cy, cr = circle
        
        # Bullseye + Ringe
        cv2.circle(frame, (cx,cy), 15, (0,0,255), 3)  # Bull
        cv2.circle(frame, (cx,cy), 35, (255,165,0), 2)  # 25
        cv2.circle(frame, (cx,cy), cr*0.4, (0,255,255), 2)  # Triple
        cv2.circle(frame, (cx,cy), cr*0.95, (255,0,255), 2)  # Double
        
        # 20 Segmente
        for i in range(20):
            angle = i * 18
            rad = math.radians(angle)
            ex = int(cx + cr * 1.1 * math.cos(rad))
            ey = int(cy + cr * 1.1 * math.sin(rad))
            cv2.line(frame, (cx,cy), (ex,ey), (128,128,128), 2)
        
        return frame

    def run_demo(self):
        self.init_cameras()
        print("INNOWEEK DART-SCORING LIVE")
        print("q=Quit, r=Reset")
        
        while True:
            frames = []
            total_darts = 0
            
            for i, cap in enumerate(self.vidcaps):
                ret, frame = cap.read()
                if not ret:
                    continue
                
                # Scheibe finden
                circle = self.find_board_circle(frame)
                self.board_circles[i] = circle
                
                # Darts erkennen
                darts = self.detect_darts(frame, circle)
                total_darts += len(darts)
                
                # Overlay
                frame = self.draw_board_overlay(frame, circle)
                
                # Darts zeichnen
                for dart in darts:
                    cv2.circle(frame, int(dart['x'], dart['y']), 12, (0,255,0), 3)
                    cv2.putText(frame, str(dart['score']), 
                               (dart['x']-25, dart['y']-25),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
                
                # Info
                cv2.rectangle(frame, (0,0), (200,100), (0,0,0), -1)
                cv2.putText(frame, self.cam_names[i], (10,30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"Darts: {len(darts)}", (10,60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
                frames.append(frame)
            
            # 3x2 Grid (perfekte Größe)
            combined = np.hstack(frames)
            cv2.putText(combined, f"INNOWEek TOTAL DARTS: {total_darts}", 
                       (20,50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
            
            cv2.imshow('INNOWEEK DART-SCORING', combined)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if key == ord('r'):
                self.dart_scores = [0,0,0]
        
        for cap in self.vidcaps:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    scorer = InnoweekDartScorer()
    scorer.run_demo