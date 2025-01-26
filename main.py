# main.py
import cv2
from deepface import DeepFace
import time
from patients import patients

# Initialize webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
REVIEW_INTERVAL = 30  # 5 minutes (adjust to 30 seconds for testing)
last_review_time = time.time()
patient_ids = list(patients.keys())
current_patient_idx = 0
# main.py additions
QUEBEC_COLORS = {
    "Blue": (255, 0, 0),     # BGR color format
    "Red": (0, 0, 255),
    "Yellow": (0, 255, 255),
    "Green": (0, 255, 0),
    "White": (255, 255, 255)
}

def display_quebec_status(frame, triage_result):
    """Show Quebec triage status on camera feed"""
    # Color background
    cv2.rectangle(frame, (0,0), (frame.shape[1], 40), QUEBEC_COLORS[triage_result["color"]], -1)
    
    # Status text
    status_text = f"{triage_result['level']} - {triage_result['action']} (Wait: {triage_result['wait_time']}m)"
    cv2.putText(frame, status_text, (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    
    # Priority reason
    cv2.putText(frame, triage_result["reason"], (10, 60),
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
    
    return frame

def analyze_patient(patient_id):
    ret, frame = cap.read()
    if not ret:
        return
    
    # Convert BGR to RGB (DeepFace compatibility)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    try:
        emotion = DeepFace.analyze(
            img_path=rgb_frame,  # Use RGB array directly
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )[0]['dominant_emotion']
        patients[patient_id]["emotion_log"].append({
            "time": time.time(),
            "emotion": emotion
        })
        print(f"✅ {patient_id}: Logged '{emotion}'")
        
    except Exception as e:
        print(f"❌ {patient_id} analysis failed:", str(e))

try:
    while True:
        # Trigger review every 5 minutes
        if time.time() - last_review_time >= REVIEW_INTERVAL:
            print(f"\n=== STARTING PATIENT REVIEW ({time.ctime()}) ===")
            
            # Analyze current patient
            patient_id = patient_ids[current_patient_idx]
            print(f"Reviewing {patient_id}...")
            analyze_patient(patient_id)
            
            # Move to next patient (cyclic)
            current_patient_idx = (current_patient_idx + 1) % len(patient_ids)
            last_review_time = time.time()
            print(f"Next patient: {patient_ids[current_patient_idx]} (in 5 mins)")
            print("=== REVIEW COMPLETE ===\n")

        # Inside the while loop:
        triage_result = {
        "level": "II",
        "color": "Red",
        "action": "Emergent",
        "reason": "Mocked: Chest pain detected",
        "wait_time": 15
        }
        frame = display_quebec_status(frame, triage_result)
        
        # Optional: Show live feed (press 'q' to exit)
        ret, frame = cap.read()
        if ret:
            cv2.imshow('ER Triage Monitor', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()