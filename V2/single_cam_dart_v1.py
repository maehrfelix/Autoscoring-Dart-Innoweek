import cv2
import numpy as np
import time
import math

CAM_ID = 1  # anpassen, wenn nötig
WINDOW_NAME = "SingleCam Dart v1"

# ---------- Hilfsfunktionen ----------

def capture_frame(cam_id, text):
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    cap.set(3, 1280)
    cap.set(4, 720)
    time.sleep(1.5)

    print(text)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        disp = frame.copy()
        cv2.putText(disp, text + " (Leertaste = Bild, q = Abbruch)",
                    (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
        cv2.imshow(WINDOW_NAME, disp)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            cap.release()
            cv2.destroyAllWindows()
            return frame
        if key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return None

def detect_board_circle(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    rows = gray.shape[0]

    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1.2, rows/8,
        param1=100, param2=30,
        minRadius=int(rows*0.25),
        maxRadius=int(rows*0.48)
    )
    if circles is None:
        return None
    circles = np.uint16(np.around(circles))
    # nimm größten Kreis
    circle = max(circles[0,:], key=lambda c: c[2])
    x, y, r = int(circle[0]), int(circle[1]), int(circle[2])
    return x, y, r

def find_dart_tip(img_before, img_after, board_circle):
    bx, by, br = board_circle
    # Absolutdifferenz
    diff = cv2.absdiff(img_before, img_after)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 25, 255, cv2.THRESH_BINARY)
    # Board-Maske anwenden
    mask = np.zeros_like(thresh)
    cv2.circle(mask, (bx,by), int(br*1.05), 255, -1)
    thresh = cv2.bitwise_and(thresh, thresh, mask=mask)

    # Morphologie
    kernel = np.ones((3,3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, thresh

    # Größte Kontur (neuer Dart)
    cnt = max(contours, key=cv2.contourArea)
    if cv2.contourArea(cnt) < 50:
        return None, thresh

    # Spitze = Punkt, der dem Mittelpunkt am nächsten ist (oder am weitesten, je nach Blickrichtung)
    pts = cnt.reshape(-1,2)
    dists = np.linalg.norm(pts - np.array([bx,by]), axis=1)
    tip_idx = np.argmin(dists)   # nahe am Zentrum
    tip = pts[tip_idx]
    return (int(tip[0]), int(tip[1])), thresh

def score_from_point(tip, board_circle):
    bx, by, br = board_circle
    tx, ty = tip
    dx = tx - bx
    dy = by - ty  # invert Y für mathem. Winkel
    r = math.hypot(dx, dy)
    angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

    # Segment bestimmen (0–19)
    # Start bei 6 Uhr = 0°, im Uhrzeigersinn
    # mapping wie Standard-Board:
    number_order = [6,13,4,18,1,20,5,12,9,14,11,8,16,7,19,3,17,2,15,10]  # Beispiel, ggf. anpassen
    seg = int((angle + 9) // 18) % 20
    base_number = number_order[seg]

    # Ring bestimmen
    # grob: Bull, 25, Single, Triple, Single, Double
    rbull = br*0.03
    r25  = br*0.07
    rtriple_in  = br*0.45
    rtriple_out = br*0.50
    rdouble_in  = br*0.95
    rdouble_out = br*1.00

    if r <= rbull:
        return 50
    elif r <= r25:
        return 25
    elif rtriple_in <= r <= rtriple_out:
        return base_number*3
    elif rdouble_in <= r <= rdouble_out:
        return base_number*2
    elif r > rdouble_out:
        return 0
    else:
        return base_number

# ---------- Hauptprogramm ----------

def main():
    # 1) Referenzbild
    img_before = capture_frame(CAM_ID, "Board OHNE Dart aufnehmen")
    if img_before is None:
        return

    # 2) Bild mit Dart
    img_after = capture_frame(CAM_ID, "Board MIT Dart aufnehmen")
    if img_after is None:
        return

    # 3) Scheibe erkennen
    circle = detect_board_circle(img_before)
    if circle is None:
        print("Dartscheibe wurde nicht erkannt.")
        return
    bx, by, br = circle
    print(f"Board-Kreis: center=({bx},{by}), r={br}")

    # 4) Dartspitze finden
    tip, diff_vis = find_dart_tip(img_before, img_after, circle)
    if tip is None:
        print("Kein Dart erkannt.")
        cv2.imshow("Diff", diff_vis)
        cv2.waitKey(0)
        return

    # 5) Score berechnen
    sc = score_from_point(tip, circle)
    print(f"Dart Spitze bei {tip}, Score ~ {sc}")

    # 6) Visualisierung
    vis = img_after.copy()
    cv2.circle(vis, (bx,by), br, (255,0,255), 2)
    cv2.circle(vis, tip, 8, (0,0,255), -1)
    cv2.putText(vis, f"Score: {sc}", (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)
    cv2.imshow("Ergebnis", vis)
    cv2.imshow("Diff", diff_vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
