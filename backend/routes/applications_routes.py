from flask import Blueprint, request, jsonify
from utils.db import get_db_connection
import psycopg2
import psycopg2.extras

applications_bp = Blueprint('applications', __name__, url_prefix='/api/applications')

@applications_bp.route('/me', methods=['GET'])
def my_applications():
    """Return applications for the given username (from header or query)."""
    username = request.headers.get('X-Username') or request.args.get('username')
    if not username:
        return jsonify({'error': 'username required'}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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
            """
            SELECT trial_type, eligibility, created_at
            FROM applications
            WHERE username = %s
            ORDER BY created_at DESC
            """,
            (username,)
        )
        rows = cursor.fetchall()
        return jsonify({'applications': rows}), 200
    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()