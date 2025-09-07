import pandas as pd

def filter_features_for_model(input_data, model_name):
    """
    Filter input data to only include features required by the specific ML model.
    Handles case variations, extra columns, and missing values.
    """

    model_features = {
        'hypertension': [
            'age', 'gender', 'bmi', 'glucose', 'lifestyle_risk', 'stress_level',
            'systolic_bp', 'diastolic_bp', 'cholesterol_total', 'comorbidities', 'consent'
        ],
        'arthritis': [
            'age', 'years_since_diagnosis', 'tender_joint_count', 'swollen_joint_count',
            'crp_level', 'patient_pain_score', 'egfr', 'on_biologic_dmards', 'has_hepatitis'
        ],
        'migraine': [
            'age', 'migraine_frequency', 'previous_medication_failures', 'liver_enzyme_level',
            'has_aura', 'chronic_kidney_disease', 'on_anticoagulants', 'sleep_disorder',
            'depression', 'caffeine_intake'
        ],
        'phase1': [
            'age', 'sex', 'weight_kg', 'height_cm', 'bmi', 'cohort',
            'alt', 'creatinine', 'sbp', 'dbp', 'hr', 'temp_c', 'adverse_event'
        ]
    }

    required_features = model_features.get(model_name)
    if not required_features:
        raise ValueError(f"Unknown model name: {model_name}")

    feature_mappings = {
        'age': ['age', 'Age', 'AGE', 'patient_age'],
        'gender': ['gender', 'Gender', 'GENDER', 'sex', 'Sex', 'SEX'],
        'bmi': ['bmi', 'BMI', 'body_mass_index', 'Body_Mass_Index'],
        'glucose': ['glucose', 'Glucose', 'GLUCOSE', 'blood_glucose', 'Blood_Glucose'],
        'lifestyle_risk': ['lifestyle_risk', 'Lifestyle_Risk', 'lifestyle_risk_level'],
        'stress_level': ['stress_level', 'Stress_Level', 'stress'],
        'systolic_bp': ['systolic_bp', 'Systolic_BP', 'sbp', 'SBP', 'systolic'],
        'diastolic_bp': ['diastolic_bp', 'Diastolic_BP', 'dbp', 'DBP', 'diastolic'],
        'cholesterol_total': ['cholesterol_total', 'Cholesterol_Total', 'total_cholesterol'],
        'comorbidities': ['comorbidities', 'Comorbidities', 'comorbidity_count'],
        'consent': ['consent', 'Consent', 'CONSENT'],

        'years_since_diagnosis': ['years_since_diagnosis', 'Years_Since_Diagnosis'],
        'tender_joint_count': ['tender_joint_count', 'Tender_Joint_Count'],
        'swollen_joint_count': ['swollen_joint_count', 'Swollen_Joint_Count'],
        'crp_level': ['crp_level', 'CRP_Level', 'crp', 'CRP'],
        'patient_pain_score': ['patient_pain_score', 'Patient_Pain_Score', 'pain_score'],
        'egfr': ['egfr', 'eGFR', 'EGFR'],
        'on_biologic_dmards': ['on_biologic_dmards', 'On_Biologic_DMARDs', 'biologic_dmards'],
        'has_hepatitis': ['has_hepatitis', 'Has_Hepatitis', 'hepatitis'],

        'migraine_frequency': ['migraine_frequency', 'Migraine_Frequency'],
        'previous_medication_failures': ['previous_medication_failures', 'Previous_Medication_Failures'],
        'liver_enzyme_level': ['liver_enzyme_level', 'Liver_Enzyme_Level'],
        'has_aura': ['has_aura', 'Has_Aura', 'aura'],
        'chronic_kidney_disease': ['chronic_kidney_disease', 'Chronic_Kidney_Disease'],
        'on_anticoagulants': ['on_anticoagulants', 'On_Anticoagulants'],
        'sleep_disorder': ['sleep_disorder', 'Sleep_Disorder'],
        'depression': ['depression', 'Depression'],
        'caffeine_intake': ['caffeine_intake', 'Caffeine_Intake'],

        'sex': ['sex', 'Sex', 'SEX', 'gender', 'Gender'],
        'weight_kg': ['weight_kg', 'Weight_kg', 'weight', 'Weight'],
        'height_cm': ['height_cm', 'Height_cm', 'height', 'Height'],
        'cohort': ['cohort', 'Cohort'],
        'alt': ['alt', 'ALT'],
        'creatinine': ['creatinine', 'Creatinine'],
        'hr': ['hr', 'HR', 'heart_rate', 'Heart_Rate'],
        'temp_c': ['temp_c', 'Temp_C', 'temperature', 'Temperature'],
        'adverse_event': ['adverse_event', 'Adverse_Event', 'AdverseEvent']
    }

    filtered_data = {}

    for feature in required_features:
        value = None
        possible_keys = feature_mappings.get(feature, [feature])

        for possible_key in possible_keys:
            if possible_key in input_data:
                value = input_data[possible_key]
                break

        if value is None or (isinstance(value, float) and pd.isna(value)):
            if feature in ['gender', 'consent']:
                value = 'Male' if feature == 'gender' else 'Yes'
            elif feature in ['sex']:
                value = 0
            elif feature in ['on_biologic_dmards', 'has_hepatitis', 'has_aura',
                             'chronic_kidney_disease', 'on_anticoagulants',
                             'sleep_disorder', 'depression', 'adverse_event']:
                value = 0
            else:
                value = 0

            print(f"⚠️ Missing feature '{feature}' for {model_name}, using default: {value}")

        filtered_data[feature] = value

    print(f"🔍 Filtered {len(filtered_data)} features for {model_name}: {list(filtered_data.keys())}")
    return filtered_data
