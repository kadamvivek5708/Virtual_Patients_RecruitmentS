from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import get_db_connection
import psycopg2
import psycopg2.extras


auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user_type = data.get('user_type', 'patient')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = "INSERT INTO users (username, password_hash, user_type) VALUES (%s, %s, %s) RETURNING id"
        cursor.execute(query, (username, hashed_password, user_type))
        
        user_id = cursor.fetchone()[0]
        
        conn.commit()
        
        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 201
    
    except psycopg2.IntegrityError:
        if conn:
            conn.rollback()
        return jsonify({'error': 'Username already exists'}), 409
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return jsonify({'error': f'Database error: {e}'}), 500
        
    finally:
        if conn:
            cursor.close()
            conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password_hash'], password):
            try:
                # Update last_login
                cursor2 = conn.cursor()
                cursor2.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMPTZ NULL")
                cursor2.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (user['id'],))
                conn.commit()
                cursor2.close()
            except Exception:
                conn.rollback()
            return jsonify({
                'message': 'Login successful',
                'user_id': user['id'],
                'username': user['username'],
                'user_type': user['user_type']
            }), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {e}'}), 500
        
    finally:
        if conn:
            cursor.close()
            conn.close()