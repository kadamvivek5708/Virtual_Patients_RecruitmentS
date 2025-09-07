import pickle
import os
import traceback
import pandas as pd
from config import MODEL_PATHS
from utils.feature_filter import filter_features_for_model

MODELS = {}

def load_models():
    """Load all ML models on startup"""
    global MODELS
    for model_name, path in MODEL_PATHS.items():
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    MODELS[model_name] = pickle.load(f)
                print(f"✓ Loaded {model_name} model successfully")
            except Exception as e:
                print(f"❌ Error loading {model_name}: {e}")
        else:
            print(f"⚠ Warning: {model_name} model file not found at {path}")
    print(f"📊 Total models loaded: {len(MODELS)}")
    return len(MODELS)


def predict_eligibility(model_name, features):
    """Predict eligibility using the specified model with proper column names and data types"""
    if model_name not in MODELS:
        print(f"❌ Model {model_name} not found in loaded models")
        return 'Ineligible'

    try:
        # Filter features to only include what the model expects
        filtered_features = filter_features_for_model(features, model_name)

        print(f"🔍 Original features count: {len(features)}")
        print(f"🔍 Filtered features count: {len(filtered_features)}")
        print(f"🔍 Filtered features: {list(filtered_features.keys())}")

        # Create DataFrame with model-specific column names and data types
        if model_name == 'hypertension':
            feature_df = pd.DataFrame([{
                'Age': int(filtered_features['age']),
                'Gender': str(filtered_features['gender']),
                'BMI': float(filtered_features['bmi']),
                'Glucose': float(filtered_features['glucose']),
                'Lifestyle_Risk': int(filtered_features['lifestyle_risk']),
                'Stress_Level': int(filtered_features['stress_level']),
                'Systolic_BP': int(filtered_features['systolic_bp']),
                'Diastolic_BP': int(filtered_features['diastolic_bp']),
                'Cholesterol_Total': float(filtered_features['cholesterol_total']),
                'Comorbidities': int(filtered_features['comorbidities']),
                'Consent': str(filtered_features['consent'])
            }])

        elif model_name == 'arthritis':
            feature_df = pd.DataFrame([{
                'Age': int(filtered_features['age']),
                'Years_Since_Diagnosis': float(filtered_features['years_since_diagnosis']),
                'Tender_Joint_Count': int(filtered_features['tender_joint_count']),
                'Swollen_Joint_Count': int(filtered_features['swollen_joint_count']),
                'CRP_Level': float(filtered_features['crp_level']),
                'Patient_Pain_Score': int(filtered_features['patient_pain_score']),
                'eGFR': float(filtered_features['egfr']),
                'On_Biologic_DMARDs': int(filtered_features['on_biologic_dmards']),
                'Has_Hepatitis': int(filtered_features['has_hepatitis'])
            }])

        elif model_name == 'migraine':
            feature_df = pd.DataFrame([{
                'Age': int(filtered_features['age']),
                'Migraine_Frequency': int(filtered_features['migraine_frequency']),
                'Previous_Medication_Failures': int(filtered_features['previous_medication_failures']),
                'Liver_Enzyme_Level': float(filtered_features['liver_enzyme_level']),
                'Has_Aura': int(filtered_features['has_aura']),
                'Chronic_Kidney_Disease': int(filtered_features['chronic_kidney_disease']),
                'On_Anticoagulants': int(filtered_features['on_anticoagulants']),
                'Sleep_Disorder': int(filtered_features['sleep_disorder']),
                'Depression': int(filtered_features['depression']),
                'Caffeine_Intake': int(filtered_features['caffeine_intake'])
            }])

        elif model_name == 'phase1':
            # Encode categorical variables
            sex_value = str(filtered_features['sex']).upper()
            sex_numeric = 1 if sex_value in ['F', 'FEMALE', '1'] else 0

            cohort_value = str(filtered_features['cohort']).lower()
            cohort_mapping = {
                'placebo': 0, 'dose_1': 1, 'dose_2': 2, 'dose_3': 3,
                'treatment': 1, 'control': 0, 'dose1': 1, 'dose2': 2, 'dose3': 3
            }
            try:
                cohort_numeric = int(float(filtered_features['cohort']))
            except (ValueError, TypeError):
                cohort_numeric = cohort_mapping.get(cohort_value, 0)

            adverse_value = str(filtered_features['adverse_event']).lower()
            if adverse_value in ['yes', 'true', '1', 'y']:
                adverse_numeric = 1
            else:
                try:
                    adverse_numeric = int(float(filtered_features['adverse_event']))
                except (ValueError, TypeError):
                    adverse_numeric = 0

            feature_df = pd.DataFrame([{
                'age': float(filtered_features['age']),
                'sex': sex_numeric,
                'weight_kg': float(filtered_features['weight_kg']),
                'height_cm': float(filtered_features['height_cm']),
                'bmi': float(filtered_features['bmi']),
                'cohort': cohort_numeric,
                'alt': float(filtered_features['alt']),
                'creatinine': float(filtered_features['creatinine']),
                'sbp': float(filtered_features['sbp']),
                'dbp': float(filtered_features['dbp']),
                'hr': float(filtered_features['hr']),
                'temp_c': float(filtered_features['temp_c']),
                'adverse_event': adverse_numeric
            }])

        else:
            feature_df = pd.DataFrame([filtered_features])

        print(f"🔍 DataFrame columns: {feature_df.columns.tolist()}")
        print(f"🔍 DataFrame dtypes: {feature_df.dtypes.to_dict()}")
        print(f"🔍 DataFrame values: {feature_df.values.tolist()}")

        model = MODELS[model_name]
        prediction = model.predict(feature_df)[0]
        result = 'Eligible' if prediction == 1 else 'Ineligible'

        print(f"✓ Prediction for {model_name}: {result}")
        return result

    except Exception as e:
        print(f"❌ Prediction error for {model_name}: {e}")
        traceback.print_exc()
        return 'Ineligible'
