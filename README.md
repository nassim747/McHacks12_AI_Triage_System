# ER Triage Optimization System

## The problem: basically our terrible healthcare system
In Quebec, ER wait times often exceed **5+ hours**, particularly for non-urgent cases. While some cases may initially appear non-urgent, they can rapidly escalate without timely intervention. Overwhelmed medical staff may miss critical changes, leading to preventable tragedies.

## Our Solution
We've developed an **AI-powered triage optimization system** that:
1. **Monitors Patient Emotions**: Uses facial recognition (via DeepFace) to detect emotional changes in waiting patients
2. **Dynamic Triage Adjustment**: Combines emotional data with medical history to recommend priority changes
3. **Quebec-Compliant**: Implements official Quebec triage levels (I-V) with real-time escalation

## Key Features
- **Real-Time Emotion Analysis**: Detects distress signals (fear, pain) through facial expressions
- **Priority Escalation**: Automatically adjusts triage levels based on:
  - Emotional state changes
  - Wait time thresholds
  - Medical history (age, chronic conditions)
- **Visual Alerts**: Color-coded status display matching Quebec hospital standards

## Technology Stack
- **Facial Recognition**: [DeepFace](https://github.com/serengil/deepface) (Open Source)
- **AI Triage**: DeepSeek API (Medical-grade LLM)
- **Visualization**: OpenCV (Real-time camera feed overlay)
- **Backend**: Python

## Installation
1. Clone the repository:
   git clone https://github.com/nassim747/McHacks12_AI_Triage_System
