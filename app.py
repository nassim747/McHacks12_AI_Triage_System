from flask import Flask, jsonify
from llm_triage import evaluate_patient
from patients import patients

app = Flask(__name__)

@app.route('/api/patients')
def get_patients():
    return jsonify({
        pid: evaluate_patient(pid) 
        for pid in patients.keys()
    })

if __name__ == '__main__':
    app.run(debug=True).p