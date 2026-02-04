import cv2
import numpy as np

IMG_FILE = "board_debug.png"

def main():
    # --- Bild laden ---
    img = cv2.imread(IMG_FILE)
    if img is None:
        print("Kein Bild", IMG_FILE)
        return

    h, w = img.shape[:2]
    print("Bildgröße:", w, "x", h)

    # --- ROI definieren: nur Bereich um die Scheibe ---
    # hier: vertikal mittleres Drittel, horizontal mittlere 70 %
    x1 = int(w * 0.15)
    x2 = int(w * 0.85)
    y1 = int(h * 0.25)
    y2 = int(h * 0.95)

    roi = img[y1:y2, x1:x2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    rh, rw = gray.shape
    print("ROI:", rw, "x", rh)

    # --- HoughCircles NUR in der ROI ---
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=rh/2,
        param1=120,
        param2=40,
        minRadius=int(rh*0.25),
        maxRadius=int(rh*0.55)
    )

    vis = img.copy()
    best = None

    if circles is not None:
        circles = np.uint16(np.around(circles[0]))
        print("Kreise in ROI:", len(circles))

        # Kreis in Bildkoordinaten transformieren und filtern
        candidates = []
        for (cx, cy, r) in circles:
            gx = cx + x1
            gy = cy + y1

            # Filter: Kreiszentrum etwa im mittleren horizontalen Bereich
            if gx < w*0.25 or gx > w*0.75:
                continue
            # Filter: Kreis nicht zu klein / zu groß
            if r < rh*0.3 or r > rh*0.6:
                continue

            candidates.append((gx, gy, r))

        print("Kandidaten nach Filter:", len(candidates))

        if candidates:
            # Nimm Kandidat mit größtem Radius
            best = max(candidates, key=lambda c: c[2])
            bx, by, br = best
            cv2.circle(vis, (bx, by), br, (0, 255, 255), 3)
            cv2.circle(vis, (bx, by), 3, (0, 0, 255), -1)
        else:
            print("Keine passenden Kreise nach Filter.")

    else:
        print("Keine Kreise gefunden.")

    # ROI zur Kontrolle einzeichnen
    cv2.rectangle(vis, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imshow("Board-Erkennung v2", vis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
