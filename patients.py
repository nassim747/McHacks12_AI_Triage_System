import time  
import random  

# Predefined lists for randomization  
SYMPTOMS = ["chest pain", "headache", "shortness of breath", "vomiting", "dizziness"]  
CONDITIONS = ["diabetes", "hypertension", "asthma", "none"]  

def generate_patients(num_patients=5):  
    patients = {}  
    for i in range(1, num_patients + 1):  
        patient_id = f"PT{str(i).zfill(3)}"  # PT001, PT002, etc.  
        patients[patient_id] = {  
            "age": random.randint(18, 90),  
            "chronic_conditions": random.sample(CONDITIONS, k=random.randint(0, 2)),  
            "symptoms": random.sample(SYMPTOMS, k=random.randint(1, 3)),  
            "emotion_log": [],  
            "arrival_time": time.time() - random.randint(300, 54000)  # 5m to 15h ago  
        }  
        # Ensure "none" isn't paired with other conditions  
        if "none" in patients[patient_id]["chronic_conditions"]:  
            patients[patient_id]["chronic_conditions"] = ["none"]  
    return patients  

# Generate 10 patients  
patients = generate_patients(10)
# Update predefined patients:
patients["CRIT001"] = {  
    "age": 68,  
    "chronic_conditions": ["diabetes", "hypertension"],  
    "symptoms": ["chest pain", "sweating"],  
    "emotion_log": [  # FIXED FORMAT
        {"time": time.time() - 1800, "emotion": "pain"},
        {"time": time.time() - 1700, "emotion": "fear"},
        {"time": time.time() - 1600, "emotion": "pain"}
    ],  
    "arrival_time": time.time() - 1800
}

patients["LONGWAIT001"] = {  
    "age": 45,  
    "chronic_conditions": ["none"],  
    "symptoms": ["headache"],  
    "emotion_log": [{"time": time.time() - i*300, "emotion": "neutral"} for i in range(5)],  
    "arrival_time": time.time() - 8500
}
