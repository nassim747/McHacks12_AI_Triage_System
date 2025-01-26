# test_triage.py
from llm_triage import evaluate_patient
from patients import patients
import time

# Force test data
patients["TEST001"] = {
    "age": 70,
    "chronic_conditions": ["diabetes"],
    "symptoms": ["chest pain"],
    "emotion_log": [{"emotion": "fear"}, {"emotion": "sad"}],
    "arrival_time": time.time() - 1200  # 20 mins ago
}

result = evaluate_patient("TEST001")
print("Triage Result:", result)

# Add assertions to validate output structure
assert "level" in result, "Missing triage level"
assert result["level"] in ["I", "II", "III", "IV", "V"], f"Invalid level: {result['level']}"
print("✅ Test passed - valid triage structure")