import json
import requests
from patients import patients
from dotenv import load_dotenv
import os
import time 

load_dotenv()
API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv('DEEP_SEEK_API_KEY')

def evaluate_patient(patient_id):
    patient = patients[patient_id]
    wait_mins = int((time.time() - patient["arrival_time"])/60)
    last_emotions = [e["emotion"] for e in patient["emotion_log"][-3:]]
    current_emotion = patient["emotion_log"][-1]["emotion"] if patient["emotion_log"] else "neutral"
    
    prompt = f"""**Quebec ER Triage Protocol - Emotion-Mandatory System**
1. Level I (Blue): Cardiac arrest/major trauma (any emotion)
2. Level II (Red): Life-threatening symptoms (chest pain, stroke) + pain/fear
3. Level III (Yellow): Severe symptoms (fractures, fever) + distress
4. Level IV (Green): Non-critical symptoms + calm/neutral
5. Level V (White): Minor issues

**Mandatory Rules:**
- Level II REQUIRES BOTH:
  - Critical symptoms (chest pain, etc.) 
  - Real-time emotion = pain/fear + ≥2 distress entries in history
- Neutral/happy emotions DOWNGRADE by 1 level
- Waiting time only considered within same urgency tier

**Patient Data:**
- ID: {patient_id}
- Symptoms: {", ".join(patient['symptoms'])}
- Conditions: {", ".join(patient['chronic_conditions'])}
- Real-Time Emotion: {current_emotion}
- Emotional History: {last_emotions}
- Wait Time: {wait_mins}m

**Output JSON with:**
- "level": I-V
- "color": Blue/Red/Yellow/Green/White
- "action": [Action]
- "reason": Must explicitly mention emotions if Level I-II"""

    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        triage_data = json.loads(response.json()["choices"][0]["message"]["content"])
        
        # Validation: Downgrade if critical level lacks emotion justification
        if triage_data["level"] in ["I", "II"]:
            emotion_keywords = ["pain", "fear", "distress"]
            if not any(kw in triage_data["reason"].lower() for kw in emotion_keywords):
                new_level = min(int(triage_data["level"]) + 1, 5)
                triage_data["level"] = str(new_level)
                triage_data["color"] = ["Blue", "Red", "Yellow", "Green", "White"][new_level-1]
                triage_data["reason"] += " [Auto-Downgrade: No emotional distress detected]"
        
        triage_data["wait_time"] = wait_mins
        triage_data["last_review"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return triage_data
        
    except Exception as e:
        print(f"DeepSeek Error: {str(e)}")
        return {"level": "V", "color": "White", "action": "Error", "reason": "System unavailable"}
