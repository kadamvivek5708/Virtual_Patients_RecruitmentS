from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.query_builder import execute_query
from models.ml_models import predict_eligibility
import traceback
import psycopg2

patient_bp = Blueprint('patient', __name__, url_prefix='/api/patient')


def validate_patient_data(trial_type, data):
    """Server-side validation for required fields and ranges aligned with schema."""
    # Define validation rules matching routes/trial_routes.py and DB schema
    rules = {
        'hypertension': [
            ('age', int, 18, 100),
            ('gender', str, None, None),
            ('bmi', float, 10, 60),
            ('glucose', float, 50, 500),
            ('lifestyle_risk', int, 0, 10),
            ('stress_level', int, 0, 10),
            ('systolic_bp', int, 80, 240),
            ('diastolic_bp', int, 40, 140),
            ('cholesterol_total', float, 100, 400),
            ('comorbidities', int, 0, 10),
            ('consent', str, None, None),
        ],
        'arthritis': [
            ('age', int, 18, 100),
            ('years_since_diagnosis', float, 0, 80),
            ('tender_joint_count', int, 0, 100),
            ('swollen_joint_count', int, 0, 100),
            ('crp_level', float, 0, 300),
            ('patient_pain_score', int, 0, 10),
            ('egfr', float, 0, 200),
            ('on_biologic_dmards', int, 0, 1),
            ('has_hepatitis', int, 0, 1),
        ],
        'migraine': [
            ('age', int, 18, 80),
            ('migraine_frequency', int, 0, 30),
            ('previous_medication_failures', int, 0, 10),
            ('liver_enzyme_level', float, 0, 500),
            ('has_aura', int, 0, 1),
            ('chronic_kidney_disease', int, 0, 1),
            ('on_anticoagulants', int, 0, 1),
            ('sleep_disorder', int, 0, 1),
            ('depression', int, 0, 1),
            ('caffeine_intake', int, 0, 20),
        ],
        'phase1': [
            ('age', int, 18, 80),
            ('sex', int, 0, 1),
            ('weight_kg', float, 30, 250),
            ('height_cm', float, 120, 220),
            ('bmi', float, 10, 60),
            ('cohort', int, 1, 10),
            ('alt', float, 0, 500),
            ('creatinine', float, 0, 20),
            ('sbp', int, 80, 240),
            ('dbp', int, 40, 140),
            ('hr', int, 30, 220),
            ('temp_c', float, 30, 45),
            ('adverse_event', int, 0, 1),
        ],
    }

    if trial_type not in rules:
        return False, [f"Unsupported trial type: {trial_type}"]

    errors = []
    for field, ftype, min_v, max_v in rules[trial_type]:
        if field not in data or data[field] in (None, ""):
            errors.append(f"Missing required field: {field}")
            continue
        try:
            # Cast to required type
            if ftype is int:
                value = int(float(data[field]))  # handle numeric strings
            elif ftype is float:
                value = float(data[field])
            else:
                value = str(data[field]).strip()
        except (ValueError, TypeError):
            errors.append(f"Invalid type for {field}")
            continue

        if min_v is not None and value < min_v:
            errors.append(f"{field} must be >= {min_v}")
        if max_v is not None and value > max_v:
            errors.append(f"{field} must be <= {max_v}")

    return len(errors) == 0, errors


@patient_bp.route('/apply', methods=['POST'])
def patient_apply():
    """Handle patient application"""
    try:
        print("📥 Received patient application request")
        data = request.json
        trial_type = data.get('trial_type')
        patient_data = data.get('patient_data')

        if not trial_type or not patient_data:
            return jsonify({"error": "Missing trial_type or patient_data"}), 400

        # Validate before processing
        ok, errors = validate_patient_data(trial_type, patient_data)
        if not ok:
            return jsonify({"error": "Validation failed", "details": errors}), 400

        eligibility = predict_eligibility(trial_type, patient_data)
        print(f"🔍 Predicted eligibility: {eligibility}")

        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        table_config = execute_query(trial_type, patient_data, eligibility, 'Patient')
        if not table_config:
            return jsonify({"error": f"Unsupported trial type: {trial_type}"}), 400

        try:
            cursor.execute(table_config['query'], table_config['values'])
            # Fetch the returned ID
            patient_id = cursor.fetchone()[0]
            
            # Audit: store application summary linked to username if available
            try:
                username = request.headers.get('X-Username') or request.args.get('username') or request.json.get('username')
                if username:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS applications (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(80) NOT NULL,
                            trial_type VARCHAR(50) NOT NULL,
                            patient_record_id INT NOT NULL,
                            eligibility VARCHAR(20) NOT NULL,
                            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                        )
                        """
                    )
                    cursor.execute(
                        "INSERT INTO applications (username, trial_type, patient_record_id, eligibility) VALUES (%s, %s, %s, %s)",
                        (username, trial_type, patient_id, eligibility)
                    )
            except Exception as _:
                pass

            conn.commit()
            
            print(f"✅ Stored patient {patient_id} with eligibility: {eligibility}")

            return jsonify({
                "patient_id": patient_id,
                "eligibility": eligibility,
                "message": f"Application submitted successfully. You are {eligibility.lower()}.",
                "trial_type": trial_type
            })

        except (Exception, psycopg2.Error) as db_error:
            conn.rollback()
            print(f"❌ Database error in patient_apply: {db_error}")
            traceback.print_exc()
            return jsonify({"error": "Database error occurred"}), 500

        finally:
            cursor.close()
            conn.close()


    except Exception as e:
        print(f"❌ Error in patient_apply: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
