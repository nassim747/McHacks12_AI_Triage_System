# main.py
import cv2
from deepface import DeepFace
import time
import winsound
from patients import patients
from llm_triage import evaluate_patient

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
REVIEW_INTERVAL = 10  # 10-second reviews
last_review_time = time.time()
patient_ids = list(patients.keys())
current_patient_idx = 0

def log_triage_alert(triage_result):
    emotion_keywords = ["pain", "fear", "distress"]
    has_distress = any(kw in triage_result["reason"].lower() for kw in emotion_keywords)
    
    if triage_result["level"] in ["I", "II"] and has_distress:
        print("\033[91m" + f"🚨 EMERGENCY! {triage_result['reason']}" + "\033[0m")
        winsound.Beep(1000, 500)
    else:
        color = "\033[93m" if triage_result["level"] == "III" else "\033[94m"
        print(color + f"⚠️  {triage_result['action']} - {triage_result['reason']}" + "\033[0m")

def analyze_patient(patient_id):
    ret, frame = cap.read()
    if not ret:
        return
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    try:
        emotion = DeepFace.analyze(
            img_path=rgb_frame,
            actions=['emotion'],
            enforce_detection=False,
            detector_backend='opencv'
        )[0]['dominant_emotion']
        patients[patient_id]["emotion_log"].append({
            "time": time.time(),
            "emotion": emotion
        })
        print(f"✅ {patient_id}: Detected '{emotion}'")
        
    except Exception as e:
        print(f"❌ {patient_id} analysis failed:", str(e))

try:
    while True:
        if time.time() - last_review_time >= REVIEW_INTERVAL:
            print(f"\n=== REVIEWING {patient_ids[current_patient_idx]} ===")
            analyze_patient(patient_ids[current_patient_idx])
            current_patient_idx = (current_patient_idx + 1) % len(patient_ids)
            last_review_time = time.time()

        ret, frame = cap.read()
        if ret:
            current_patient = patient_ids[current_patient_idx]
            triage_result = evaluate_patient(current_patient)
            log_triage_alert(triage_result)
            cv2.imshow('Patient Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
