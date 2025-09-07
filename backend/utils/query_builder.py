def execute_query(trial_type, patient_data, eligibility, source):
    """Execute database query for different trial types"""
    table_queries = {
        'hypertension': {
            'query': """
                INSERT INTO hypertension_patients
                (age, gender, bmi, glucose, lifestyle_risk, stress_level, systolic_bp,
                diastolic_bp, cholesterol_total, comorbidities, consent, eligibility, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
            'values': (
                int(patient_data.get('age', 0)), patient_data.get('gender', ''), float(patient_data.get('bmi', 0)),
                float(patient_data.get('glucose', 0)), int(patient_data.get('lifestyle_risk', 0)),
                int(patient_data.get('stress_level', 0)), int(patient_data.get('systolic_bp', 0)),
                int(patient_data.get('diastolic_bp', 0)), float(patient_data.get('cholesterol_total', 0)),
                int(patient_data.get('comorbidities', 0)), patient_data.get('consent', 'No'), eligibility, source
            )
        },
        'arthritis': {
            'query': """
                INSERT INTO arthritis_patients
                (age, years_since_diagnosis, tender_joint_count, swollen_joint_count, crp_level,
                patient_pain_score, egfr, on_biologic_dmards, has_hepatitis, eligibility, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
            'values': (
                int(patient_data.get('age', 0)), float(patient_data.get('years_since_diagnosis', 0)),
                int(patient_data.get('tender_joint_count', 0)), int(patient_data.get('swollen_joint_count', 0)),
                float(patient_data.get('crp_level', 0)), int(patient_data.get('patient_pain_score', 0)),
                float(patient_data.get('egfr', 0)), int(patient_data.get('on_biologic_dmards', 0)),
                int(patient_data.get('has_hepatitis', 0)), eligibility, source
            )
        },
        'migraine': {
            'query': """
                INSERT INTO migraine_patients
                (age, migraine_frequency, previous_medication_failures, liver_enzyme_level,
                has_aura, chronic_kidney_disease, on_anticoagulants, sleep_disorder,
                depression, caffeine_intake, eligibility, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
            'values': (
                int(patient_data.get('age', 0)), int(patient_data.get('migraine_frequency', 0)),
                int(patient_data.get('previous_medication_failures', 0)), float(patient_data.get('liver_enzyme_level', 0)),
                int(patient_data.get('has_aura', 0)), int(patient_data.get('chronic_kidney_disease', 0)),
                int(patient_data.get('on_anticoagulants', 0)), int(patient_data.get('sleep_disorder', 0)),
                int(patient_data.get('depression', 0)), int(patient_data.get('caffeine_intake', 0)), eligibility, source
            )
        },
        'phase1': {
            'query': """
                INSERT INTO phase1_patients
                (age, sex, weight_kg, height_cm, bmi, cohort, alt, creatinine,
                sbp, dbp, hr, temp_c, adverse_event, eligibility, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
            'values': (
                int(patient_data.get('age', 0)), int(patient_data.get('sex', 0)), float(patient_data.get('weight_kg', 0)),
                float(patient_data.get('height_cm', 0)), float(patient_data.get('bmi', 0)), int(patient_data.get('cohort', 0)),
                float(patient_data.get('alt', 0)), float(patient_data.get('creatinine', 0)), int(patient_data.get('sbp', 0)),
                int(patient_data.get('dbp', 0)), int(patient_data.get('hr', 0)), float(patient_data.get('temp_c', 0)),
                int(patient_data.get('adverse_event', 0)), eligibility, source
            )
        }
    }

    return table_queries.get(trial_type)
