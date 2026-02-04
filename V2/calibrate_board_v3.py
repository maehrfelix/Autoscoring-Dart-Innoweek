import cv2
import numpy as np
import math

IMG_FILE = "board_debug.png"

points = []

def mouse_callback(event, x, y, flags, param):
    global points, img_vis
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x,y))
        cv2.circle(img_vis, (x,y), 5, (0,255,0), -1)
        cv2.imshow("Kalibrierung", img_vis)

def main():
    global img_vis, points
    img = cv2.imread(IMG_FILE)
    if img is None:
        print("Kein Bild", IMG_FILE)
        return

    h, w = img.shape[:2]
    print("Bildgröße:", w, "x", h)

    # 1) Grobe Kreis-Erkennung (wie v2, aber nur als Start)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=h/4,
        param1=120,
        param2=40,
        minRadius=int(h*0.2),
        maxRadius=int(h*0.6)
    )

    img_vis = img.copy()
    if circles is not None:
        c = np.uint16(np.around(circles[0]))[0]
        cx, cy, r = int(c[0]), int(c[1]), int(c[2])
        print("Grobe Kreis-Schätzung:", cx, cy, r)
        cv2.circle(img_vis, (cx,cy), r, (0,255,255), 2)
        cv2.circle(img_vis, (cx,cy), 3, (0,0,255), -1)
    else:
        print("Keine Kreise gefunden – wir machen nur manuelle Kalibrierung.")

    # 2) Manuelle Korrektur: 4 Punkte auf Außenrand klicken
    print("Klicke 4 Punkte auf dem Außenrand der Scheibe (z.B. bei 12, 3, 6, 9 Uhr).")
    print("Fenster aktiv, dann 4x linke Maustaste. ESC oder q zum Abbruch.")

    cv2.namedWindow("Kalibrierung", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Kalibrierung", mouse_callback)
    cv2.imshow("Kalibrierung", img_vis)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key in (27, ord('q')):  # ESC oder q
            cv2.destroyAllWindows()
            return
        if len(points) >= 4:
            break

    cv2.destroyAllWindows()
    pts = np.array(points, dtype=np.int32)
    print("Klick-Punkte:", pts)

    # 3) Ellipse fitten (bessere Scheibenform)
    if len(pts) >= 5:
        ellipse = cv2.fitEllipse(pts)
    else:
        # notfalls Kreisschätzung
        if circles is None:
            print("Zu wenige Punkte für Ellipse und kein Kreis – Abbruch.")
            return
        ellipse = ((cx,cy), (2*r, 2*r), 0.0)

    (ex, ey), (axis_a, axis_b), angle = ellipse
    print(f"Ellipse: center=({ex:.1f},{ey:.1f}), axes=({axis_a:.1f},{axis_b:.1f}), angle={angle:.1f}")

    vis2 = img.copy()
    cv2.ellipse(vis2, ellipse, (0,255,255), 2)
    cv2.circle(vis2, (int(ex),int(ey)), 3, (0,0,255), -1)
    cv2.imshow("Gefittete Ellipse", vis2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 4) Kalibrier-Daten speichern
    calib = {
        "center": (float(ex), float(ey)),
        "axes": (float(axis_a/2), float(axis_b/2)),  # Halbachsen
        "angle": float(angle)
    }
    import json
    with open("board_calib_cam1.json", "w") as f:
        json.dump(calib, f, indent=2)
    print("Kalibrierung gespeichert in board_calib_cam1.json")

if __name__ == "__main__":
    main()
