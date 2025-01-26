import json
import requests
from patients import patients
from dotenv import load_dotenv
import os
import time 

load_dotenv()
API_URL = "https://api.deepseek.com/v1/chat/completions"
DEEPSEEK_API_KEY = os.getenv('DEEP_SEEK_API_KEY')  # Match exactly what's in .env

def evaluate_patient(patient_id):
    patient = patients[patient_id]
    wait_mins = int((time.time() - patient["arrival_time"])/60)
    last_emotions = [e["emotion"] for e in patient["emotion_log"][-3:]]
    
    prompt = f"""**Quebec ER Triage Protocol**
1. Level I (Blue): Resuscitation - Cardiac arrest, major trauma
2. Level II (Red): Emergent - Chest pain, stroke, respiratory distress  
3. Level III (Yellow): Urgent - Fractures, severe pain, high fever
4. Level IV (Green): Less-urgent - Sprains, minor infections
5. Level V (White): Non-urgent - Prescription renewals

**Prioritization Rules:**
- Primary: Medical urgency (sicker patients first)
- Secondary: Waiting time if same urgency level

**Patient Data:**
- ID: {patient_id}
- Age: {patient['age']}
- Conditions: {", ".join(patient['chronic_conditions'])}
- Symptoms: {", ".join(patient['symptoms'])}
- Emotional Signs: {last_emotions}
- Wait Time: {wait_mins} minutes

**Output JSON with:**
- "level": I-V
- "color": Blue/Red/Yellow/Green/White
- "action": Resuscitation/Emergent/Urgent/Less-urgent/Non-urgent
- "reason": Clinical justification"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
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
        
        # Add quebec-specific fields
        triage_data["wait_time"] = wait_mins
        triage_data["last_review"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return triage_data
        
    except Exception as e:
        print(f"DeepSeek Error: {str(e)}")
        return {"level": "V", "color": "White", "action": "Error", "reason": "System unavailable"}