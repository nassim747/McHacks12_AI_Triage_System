import time  
import random  

SYMPTOMS = ["chest pain", "headache", "shortness of breath", "vomiting", "dizziness"]  
CONDITIONS = ["diabetes", "hypertension", "asthma", "none"]  

def generate_patients(num_patients=5):  
    patients = {}  
    for i in range(1, num_patients + 1):  
        patient_id = f"PT{str(i).zfill(3)}"  
        patients[patient_id] = {  
            "age": random.randint(18, 90),  
            "chronic_conditions": random.sample(CONDITIONS, k=random.randint(0, 2)),  
            "symptoms": random.sample(SYMPTOMS, k=random.randint(1, 3)),  
            "emotion_log": [],  
            "arrival_time": time.time() - random.randint(300, 54000)  
        }  
        if "none" in patients[patient_id]["chronic_conditions"]:  
            patients[patient_id]["chronic_conditions"] = ["none"]  
    return patients  

patients = generate_patients(10)

# Critical Case: Chest pain WITH distress
patients["CRIT001"] = {  
    "age": 68,  
    "chronic_conditions": ["diabetes", "hypertension"],  
    "symptoms": ["chest pain", "sweating"],  
    "emotion_log": [
        {"time": time.time() - 10, "emotion": "pain"},
        {"time": time.time() - 5, "emotion": "fear"}
    ],  
    "arrival_time": time.time() - 1800
}

# Critical Case WITHOUT distress (should downgrade)
patients["CALMCRIT001"] = {  
    "age": 55,
    "chronic_conditions": ["hypertension"],
    "symptoms": ["chest pain"],
    "emotion_log": [{"time": time.time() - i*60, "emotion": "neutral"} for i in range(5)],
    "arrival_time": time.time() - 3600
}

# Non-critical WITH distress (should elevate)
patients["STRESSEDMILD001"] = {  
    "age": 35,
    "chronic_conditions": ["none"],
    "symptoms": ["headache"],
    "emotion_log": [{"time": time.time() - i*60, "emotion": "fear"} for i in range(5)],
    "arrival_time": time.time() - 7200
}
