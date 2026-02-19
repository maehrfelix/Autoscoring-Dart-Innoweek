from inference_sdk import InferenceHTTPClient
import cv2
import time
import os
import numpy as np

scores_cam0 = {
    "i1" : "i9",
    "i2" : "i13",
    "i3" : "i10",
    "i4" : "i5",
    "i5" : "i11",
    "i6" : "i1",
    "i7" : "i2",
    "i8" : "i3",
    "i9" : "i16",
    "i10" : "i18",
    "i11" : "i19",
    "i12" : "i8",
    "i13" : "i20",
    "i14" : "i7",
    "i15" : "i4",
    "i16" : "i17",
    "i17" : "i6",
    "i18" : "i12",
    "i19" : "i15",
    "i20" : "i14",
    
    "o1" : "o9",
    "o2" : "o13",
    "o3" : "o10",
    "o4" : "o5",
    "o5" : "o11",
    "o6" : "o1",
    "o7" : "o2",
    "o8" : "o3",
    "o9" : "o16",
    "o10" : "o18",
    "o11" : "o19",
    "o12" : "o8",
    "o13" : "o20",
    "o14" : "o7",
    "o15" : "o4",
    "o16" : "o17",
    "o17" : "o6",
    "o18" : "o12",
    "o19" : "o15",
    "o20" : "o14",
    
    "d1" : "d9",
    "d2" : "d13",
    "d3" : "d10",
    "d4" : "d5",
    "d5" : "d11",
    "d6" : "d1",
    "d7" : "d2",
    "d8" : "d3",
    "d9" : "d16",
    "d10" : "d18",
    "d11" : "d19",
    "d12" : "d8",
    "d13" : "d20",
    "d14" : "d7",
    "d15" : "d4",
    "d16" : "d17",
    "d17" : "d6",
    "d18" : "d12",
    "d19" : "d15",
    "d20" : "d14",
    
    "t1" : "t9",
    "t2" : "t13",
    "t3" : "t10",
    "t4" : "t5",
    "t5" : "t11",
    "t6" : "t1",
    "t7" : "t2",
    "t8" : "t3",
    "t9" : "t16",
    "t10" : "t18",
    "t11" : "t19",
    "t12" : "t8",
    "t13" : "t20",
    "t14" : "t7",
    "t15" : "t4",
    "t16" : "t17",
    "t17" : "t6",
    "t18" : "t12",
    "t19" : "t15",
    "t20" : "t14",
}
scores_cam1 = {
    "i1" : "i6",
    "i2" : "i7",
    "i3" : "i8",
    "i4" : "i15",
    "i5" : "i4",
    "i6" : "i17",
    "i7" : "i14",
    "i8" : "i12",
    "i9" : "i1",
    "i10" : "i3",
    "i11" : "i5",
    "i12" : "i18",
    "i13" : "i2",
    "i14" : "i20",
    "i15" : "i19",
    "i16" : "i9",
    "i17" : "i16",
    "i18" : "i10",
    "i19" : "i11",
    "i20" : "i13",
    
    "o1" : "o6",
    "o2" : "o7",
    "o3" : "o8",
    "o4" : "o15",
    "o5" : "o4",
    "o6" : "o17",
    "o7" : "o14",
    "o8" : "o12",
    "o9" : "o1",
    "o10" : "o3",
    "o11" : "o5",
    "o12" : "o18",
    "o13" : "o2",
    "o14" : "o20",
    "o15" : "o19",
    "o16" : "o9",
    "o17" : "o16",
    "o18" : "o10",
    "o19" : "o11",
    "o20" : "o13",
    
    "d1" : "d6",
    "d2" : "d7",
    "d3" : "d8",
    "d4" : "d15",
    "d5" : "d4",
    "d6" : "d17",
    "d7" : "d14",
    "d8" : "d12",
    "d9" : "d1",
    "d10" : "d3",
    "d11" : "d5",
    "d12" : "d18",
    "d13" : "d2",
    "d14" : "d20",
    "d15" : "d19",
    "d16" : "d9",
    "d17" : "d16",
    "d18" : "d10",
    "d19" : "d11",
    "d20" : "d13",
    
    "t1" : "t6",
    "t2" : "t7",
    "t3" : "t8",
    "t4" : "t15",
    "t5" : "t4",
    "t6" : "t17",
    "t7" : "t14",
    "t8" : "t12",
    "t9" : "t1",
    "t10" : "t3",
    "t11" : "t5",
    "t12" : "t18",
    "t13" : "t2",
    "t14" : "t20",
    "t15" : "t19",
    "t16" : "t9",
    "t17" : "t16",
    "t18" : "t10",
    "t19" : "t11",
    "t20" : "t13",

}
scores_cam3 = {
    "b" : "b",
    "sb" : "sb",
    "i1" : "i4",
    "i2" : "i3",
    "i3" : "i7",
    "i4" : "i6",
    "i5" : "i1",
    "i6" : "i15",
    "i7" : "i8",
    "i8" : "i14",
    "i9" : "i5",
    "i10" : "i2",
    "i11" : "i9",
    "i12" : "i20",
    "i13" : "i10",
    "i14" : "i12",
    "i15" : "i17",
    "i16" : "i11",
    "i17" : "i19",
    "i18" : "i13",
    "i19" : "i16",
    "i20" : "i18",
    
    "o1" : "o4",
    "o2" : "o3",
    "o3" : "o7",
    "o4" : "o6",
    "o5" : "o1",
    "o6" : "o15",
    "o7" : "o8",
    "o8" : "o14",
    "o9" : "o5",
    "o10" : "o2",
    "o11" : "o9",
    "o12" : "o20",
    "o13" : "o10",
    "o14" : "o12",
    "o15" : "o17",
    "o16" : "o11",
    "o17" : "o19",
    "o18" : "o13",
    "o19" : "o16",
    "o20" : "o18",
    
    "d1" : "d4",
    "d2" : "d3",
    "d3" : "d7",
    "d4" : "d6",
    "d5" : "d1",
    "d6" : "d15",
    "d7" : "d8",
    "d8" : "d14",
    "d9" : "d5",
    "d10" : "d2",
    "d11" : "d9",
    "d12" : "d20",
    "d13" : "d10",
    "d14" : "d12",
    "d15" : "d17",
    "d16" : "d11",
    "d17" : "d19",
    "d18" : "d13",
    "d19" : "d16",
    "d20" : "d18",
    
    "t1" : "t4",
    "t2" : "t3",
    "t3" : "t7",
    "t4" : "t6",
    "t5" : "t1",
    "t6" : "t15",
    "t7" : "t8",
    "t8" : "t14",
    "t9" : "t5",
    "t10" : "t2",
    "t11" : "t9",
    "t12" : "t20",
    "t13" : "t10",
    "t14" : "t12",
    "t15" : "t17",
    "t16" : "t11",
    "t17" : "t19",
    "t18" : "t13",
    "t19" : "t16",
    "t20" : "t18",
}

CAM_ID = 0  # Deine Kam (1-3)
INTERVAL = 2.0  # Sekunden zwischen Checks
PIXEL_MIN_THRESHOLD = 100  # Min. geänderte Pixel → Trigger
PIXEL_MAX_THRESHOLD = 2000  # Max. geänderte Pixel → Trigger
REF_FILE = "dartscheibe_ref.png"

# Crop constants (adjust to your camera/setup)
CROP_X = 60
CROP_Y = 120
CROP_W = 580
CROP_H = 360

def crop_dartboard(frame, crop_x=CROP_X, crop_y=CROP_Y, crop_w=CROP_W, crop_h=CROP_H):
    """Schneidet den Dartboard-Bereich aus dem Frame aus."""
    return frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]

def make_reference(cam_id):
    """Erstellt Referenzbild der leeren Scheibe."""
    cap = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    time.sleep(1.5)
    
    ret, ref_frame = cap.read()
    cap.release()
    
    if ret:
        ref_frame = crop_dartboard(ref_frame)
        # Save as grayscale reference to ensure single channel
        ref_gray = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(REF_FILE, ref_gray)
        print(f"Referenz gespeichert: {REF_FILE}")
        cv2.imshow("Referenz (leere Scheibe)", ref_gray)
        cv2.waitKey(3000)
        return True
    return False

def pixel_changes(ref_gray, current_gray):
    """Berechnet geänderte Pixel (absdiff + threshold)."""
    diff = cv2.absdiff(ref_gray, current_gray)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)  # Threshold anpassbar
    changed_pixels = cv2.countNonZero(thresh)
    return changed_pixels, thresh

def on_change_detected(changed_pixels, frame):
    get_score_from_images(CAM_ID, frame)
    print(f"ALARM! {changed_pixels} Pixel geändert! Dart erkannt?")
    cv2.putText(frame, f"DART! Pixels: {changed_pixels}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def get_score_from_images(cam_id, frame):
    frames = {}
    
    print("=== 3-KAM CAPTURE ===")
    
    for i, cam_num in enumerate([0, 1, 3], start=1):
        cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        time.sleep(0.5)  # Stabilisieren
        
        ret, captured_frame = cap.read()
        cap.release()
        
        if ret and captured_frame is not None:
            cam_name = f"cam_{cam_num}"
            frames[cam_name] = captured_frame
            print(f"cam {cam_name}: {captured_frame.shape}")
        else:
            print(f"cam {cam_num}")
    
    print(f"FERTIG: {len(frames)}/3 Frames")
    
    
    for cam_name, captured_frame in frames.items(): 
        cv2.imwrite(f"{cam_name}.png", captured_frame)
             
        # Sendet Bild an Inference SDK und erhält Score.
        try:
            client = InferenceHTTPClient(api_url="https://serverless.roboflow.com", api_key="0PM7XistpPMrMcA4NsqT")
            _, img_encoded = cv2.imencode('.jpg', captured_frame)
            response = client.infer(captured_frame, model_id="darts-right-7vpi7/2")
            print(f"Response von {cam_name}: {response}")
            
            # Check 1: response is not None
            if response is None:
                print(f"Kamera {cam_name}: Keine Response (None)")
                continue
            
            # Check 2: response has 'predictions' key
            if 'predictions' not in response:
                print(f"Kamera {cam_name}: Keine 'predictions' im Response")
                print(f"Response Schlüssel: {list(response.keys())}")
                continue
            
            # Check 3: predictions is not empty
            if not response['predictions']:
                print(f"Kamera {cam_name}: 'predictions' ist leer")
                continue
            
            # Check 4: first prediction has 'class' key
            if 'class' not in response['predictions'][0]:
                print(f"Kamera {cam_name}: Keine 'class' in predictions")
                print(f"Prediction Schlüssel: {list(response['predictions'][0].keys())}")
                continue
            
            score = response['predictions'][0]['class']
            if cam_id == 0:
                score = scores_cam0.get(score, score)
            elif cam_id == 1:
                score = scores_cam1.get(score, score)
            elif cam_id == 2:
                score = scores_cam3.get(score, score)
            print(f"Kamera {cam_id} erkannte Score: {score}")
            return score
        except Exception as e:
            print(f"Fehler bei Kamera {cam_name}: {e}")
            print(f"Kamera {cam_id} keine Score-Erkennung!")
            continue
    
# Hauptprogramm
ref_exists = os.path.exists(REF_FILE)
if ref_exists:
    ref_frame = cv2.imread(REF_FILE, cv2.IMREAD_GRAYSCALE)
    if ref_frame is None:
        print("FEHLER: Referenzbild kaputt/loesche es!")
        os.remove(REF_FILE)
        ref_exists = False
    else:
        # Ensure loaded reference matches expected crop size
        expected_shape = (CROP_H, CROP_W)
        if ref_frame.shape != expected_shape:
            ref_frame = cv2.resize(ref_frame, (expected_shape[1], expected_shape[0]))
        print("Referenz OK geladen!")
else:
    ref_frame = None
    
cap = cv2.VideoCapture(CAM_ID, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not ref_exists:
    print("Drücke 'r' für Referenzbild (leere Scheibe!)")
    ret, _ = cap.read()
else:
    print("Referenz gefunden, starte Detection...")

boot = True
while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera Fehler!")
        break
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        if make_reference(CAM_ID):
            ref_frame = cv2.imread(REF_FILE, cv2.IMREAD_GRAYSCALE)
            if ref_frame is not None:
                expected_shape = (CROP_H, CROP_W)
                if ref_frame.shape != expected_shape:
                    ref_frame = cv2.resize(ref_frame, (expected_shape[1], expected_shape[0]))
        continue
    elif key == ord('q'):
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_crop = crop_dartboard(gray)
    
    if ref_exists:
        changes, diff_img = pixel_changes(ref_frame, gray_crop)
        cv2.putText(frame, f"Changes: {changes}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Zeige Diff-Overlay
        diff_color = cv2.cvtColor(diff_img, cv2.COLOR_GRAY2BGR)
        # Resize diff_color to match frame size for blending
        diff_color_resized = cv2.resize(diff_color, (frame.shape[1], frame.shape[0]))
        overlay = cv2.addWeighted(frame, 0.7, diff_color_resized, 0.3, 0)
        if boot:
            time.sleep(2)  # Länger warten am Anfang
            boot = False
        if PIXEL_MIN_THRESHOLD < changes < PIXEL_MAX_THRESHOLD:
            on_change_detected(changes, overlay)
        
        cv2.imshow('Motion Detect (Diff Overlay)', overlay)
    else:
        cv2.imshow('Warte auf Referenz', frame)
    
    time.sleep(INTERVAL)  # Wartezeit

cap.release()
cv2.destroyAllWindows()
