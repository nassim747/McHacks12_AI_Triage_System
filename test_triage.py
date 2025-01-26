# test_triage.py
from llm_triage import evaluate_patient
from patients import patients
import time

def test_emotion_requirement():
    # Test critical symptoms WITHOUT distress
    patients["TEST001"] = {
        "age": 60,
        "chronic_conditions": ["diabetes"],
        "symptoms": ["chest pain"],
        "emotion_log": [{"time": time.time() - i*60, "emotion": "neutral"} for i in range(3)],
        "arrival_time": time.time() - 1200
    }
    result = evaluate_patient("TEST001")
    assert result["level"] not in ["I", "II"], "Critical alert without emotional distress!"
    print("✅ Test 1 Passed: Calm cardiac patient not escalated")

    # Test non-critical symptoms WITH distress
    patients["TEST002"] = {
        "age": 25,
        "chronic_conditions": ["none"],
        "symptoms": ["headache"],
        "emotion_log": [{"time": time.time() - i*60, "emotion": "fear"} for i in range(3)],
        "arrival_time": time.time() - 300
    }
    result = evaluate_patient("TEST002")
    assert result["level"] in ["III", "II"], "Distress not elevating mild symptoms!"
    print("✅ Test 2 Passed: Distress elevates mild symptoms")

test_emotion_requirement()
