from flask import Blueprint, jsonify

trial_bp = Blueprint('trial', __name__, url_prefix='/api')

@trial_bp.route('/trials', methods=['GET'])
def get_trials():
    trials = [
        {"id": "hypertension", "name": "Hypertension Trial", "description": "Clinical trial for hypertension treatment"},
        {"id": "arthritis", "name": "Arthritis Trial", "description": "Rheumatoid arthritis treatment study"},
        {"id": "migraine", "name": "Migraine Trial", "description": "Migraine prevention medication trial"},
        {"id": "phase1", "name": "Phase 1 Trial", "description": "Phase 1 safety and dosage study"}
    ]
    return jsonify(trials)


@trial_bp.route('/trial-fields/<trial_type>', methods=['GET'])
def get_trial_fields(trial_type):
    # Field definitions aligned with database schema and typical clinical ranges
    fields = {
        "hypertension": [
            {"name": "age", "type": "number", "label": "Age", "min": 18, "max": 100, "required": True},
            {"name": "gender", "type": "select", "label": "Gender", "options": ["Male", "Female"], "required": True},
            {"name": "bmi", "type": "number", "label": "BMI", "min": 10, "max": 60, "step": 0.1, "required": True},
            {"name": "glucose", "type": "number", "label": "Blood Glucose (mg/dL)", "min": 50, "max": 500, "required": True},
            {"name": "lifestyle_risk", "type": "number", "label": "Lifestyle Risk (0-10)", "min": 0, "max": 10, "required": True},
            {"name": "stress_level", "type": "number", "label": "Stress Level (0-10)", "min": 0, "max": 10, "required": True},
            {"name": "systolic_bp", "type": "number", "label": "Systolic BP (mmHg)", "min": 80, "max": 240, "required": True},
            {"name": "diastolic_bp", "type": "number", "label": "Diastolic BP (mmHg)", "min": 40, "max": 140, "required": True},
            {"name": "cholesterol_total", "type": "number", "label": "Total Cholesterol (mg/dL)", "min": 100, "max": 400, "required": True},
            {"name": "comorbidities", "type": "number", "label": "Comorbidities Count", "min": 0, "max": 10, "required": True},
            {"name": "consent", "type": "select", "label": "Consent", "options": ["Yes", "No"], "required": True},
        ],
        "arthritis": [
            {"name": "age", "type": "number", "label": "Age", "min": 18, "max": 100, "required": True},
            {"name": "years_since_diagnosis", "type": "number", "label": "Years Since Diagnosis", "min": 0, "max": 80, "step": 0.1, "required": True},
            {"name": "tender_joint_count", "type": "number", "label": "Tender Joint Count", "min": 0, "max": 100, "required": True},
            {"name": "swollen_joint_count", "type": "number", "label": "Swollen Joint Count", "min": 0, "max": 100, "required": True},
            {"name": "crp_level", "type": "number", "label": "CRP Level (mg/L)", "min": 0, "max": 300, "required": True},
            {"name": "patient_pain_score", "type": "number", "label": "Pain Score (0-10)", "min": 0, "max": 10, "required": True},
            {"name": "egfr", "type": "number", "label": "eGFR", "min": 0, "max": 200, "required": True},
            {"name": "on_biologic_dmards", "type": "select", "label": "On Biologic DMARDs", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "has_hepatitis", "type": "select", "label": "Has Hepatitis", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
        ],
        "migraine": [
            {"name": "age", "type": "number", "label": "Age", "min": 18, "max": 80, "required": True},
            {"name": "migraine_frequency", "type": "number", "label": "Migraine Frequency (per month)", "min": 0, "max": 30, "required": True},
            {"name": "previous_medication_failures", "type": "number", "label": "Previous Medication Failures", "min": 0, "max": 10, "required": True},
            {"name": "liver_enzyme_level", "type": "number", "label": "Liver Enzyme Level", "min": 0, "max": 500, "required": True},
            {"name": "has_aura", "type": "select", "label": "Has Aura", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "chronic_kidney_disease", "type": "select", "label": "Chronic Kidney Disease", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "on_anticoagulants", "type": "select", "label": "On Anticoagulants", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "sleep_disorder", "type": "select", "label": "Sleep Disorder", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "depression", "type": "select", "label": "Depression", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
            {"name": "caffeine_intake", "type": "number", "label": "Caffeine Intake (cups/day)", "min": 0, "max": 20, "required": True},
        ],
        "phase1": [
            {"name": "age", "type": "number", "label": "Age", "min": 18, "max": 80, "required": True},
            {"name": "sex", "type": "select", "label": "Sex", "options": [{"value": 0, "label": "Male"}, {"value": 1, "label": "Female"}], "required": True},
            {"name": "weight_kg", "type": "number", "label": "Weight (kg)", "min": 30, "max": 250, "step": 0.1, "required": True},
            {"name": "height_cm", "type": "number", "label": "Height (cm)", "min": 120, "max": 220, "step": 0.1, "required": True},
            {"name": "bmi", "type": "number", "label": "BMI", "min": 10, "max": 60, "step": 0.1, "required": True},
            {"name": "cohort", "type": "number", "label": "Cohort", "min": 1, "max": 10, "required": True},
            {"name": "alt", "type": "number", "label": "ALT", "min": 0, "max": 500, "required": True},
            {"name": "creatinine", "type": "number", "label": "Creatinine (mg/dL)", "min": 0, "max": 20, "required": True},
            {"name": "sbp", "type": "number", "label": "SBP (mmHg)", "min": 80, "max": 240, "required": True},
            {"name": "dbp", "type": "number", "label": "DBP (mmHg)", "min": 40, "max": 140, "required": True},
            {"name": "hr", "type": "number", "label": "Heart Rate (bpm)", "min": 30, "max": 220, "required": True},
            {"name": "temp_c", "type": "number", "label": "Temperature (°C)", "min": 30, "max": 45, "step": 0.1, "required": True},
            {"name": "adverse_event", "type": "select", "label": "Adverse Event", "options": [{"value": 0, "label": "No"}, {"value": 1, "label": "Yes"}], "required": True},
        ],
    }

    if trial_type not in fields:
        return jsonify({"error": "Invalid trial type"}), 400

    return jsonify(fields[trial_type])