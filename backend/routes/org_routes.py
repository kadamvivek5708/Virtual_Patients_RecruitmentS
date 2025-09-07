from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
from utils.query_builder import execute_query
from models.ml_models import predict_eligibility
import pandas as pd
import traceback
import psycopg2

org_bp = Blueprint('organization', __name__, url_prefix='/api/organization')

@org_bp.route('/upload', methods=['POST'])
def organization_upload():
    """Handle bulk file upload from organization"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files['file']
        trial_type = request.form.get('trial_type')

        if not trial_type:
            return jsonify({"error": "Trial type not specified"}), 400
        if not file or not file.filename:
            return jsonify({"error": "No file selected"}), 400

        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file)
        else:
            return jsonify({"error": "Unsupported file format. Use CSV or Excel."}), 400

        results = []
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()

        for index, row in df.iterrows():
            try:
                patient_data = row.to_dict()
                for key, value in patient_data.items():
                    if pd.isna(value):
                        patient_data[key] = 0 if key not in ['gender', 'consent'] else ''

                eligibility = predict_eligibility(trial_type, patient_data)

                table_config = execute_query(trial_type, patient_data, eligibility, 'Organization')
                if not table_config:
                    results.append({
                        "row": index + 1,
                        "error": f"Unsupported trial type: {trial_type}",
                        "eligibility": "Error"
                    })
                    continue

                cursor.execute(table_config['query'], table_config['values'])
                # Fetch the returned ID
                patient_id = cursor.fetchone()[0]

                results.append({
                    "row": index + 1,
                    "patient_id": patient_id,
                    "eligibility": eligibility,
                    "data": patient_data
                })

            except Exception as e:
                results.append({
                    "row": index + 1,
                    "error": str(e),
                    "eligibility": "Error"
                })

        conn.commit()
        cursor.close()
        conn.close()

        eligible_count = len([r for r in results if r.get('eligibility') == 'Eligible'])
        ineligible_count = len([r for r in results if r.get('eligibility') == 'Ineligible'])
        error_count = len([r for r in results if r.get('eligibility') == 'Error'])

        return jsonify({
            "message": "File processed successfully",
            "total_processed": len(results),
            "eligible": eligible_count,
            "ineligible": ineligible_count,
            "errors": error_count,
            "results": results[:100]
        })

    except Exception as e:
        print(f"❌ Error in organization_upload: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
