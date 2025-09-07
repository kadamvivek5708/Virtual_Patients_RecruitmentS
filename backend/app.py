import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env (useful for local dev; safe on Render/Vercel if provided)
load_dotenv()

# --- Local Application Imports ---
from config import DB_CONFIG, MODEL_PATHS
from models.ml_models import load_models, MODELS
from utils.db import get_db_connection
from errors.handlers import register_error_handlers
 
# --- Route Blueprints ---
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from routes.org_routes import org_bp
from routes.analytics_routes import analytics_bp
from routes.trial_routes import trial_bp
from routes.admin_routes import admin_bp
from routes.applications_routes import applications_bp

# --- App Initialization ---
app = Flask(__name__, static_folder='build', static_url_path='/')

# --- Extension Initialization ---
# Configure CORS for production. If FRONTEND_ORIGIN is set, use it; otherwise allow all (no credentials).
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
supports_credentials = frontend_origin != "*"
CORS(app, resources={r"/api/*": {"origins": frontend_origin}}, supports_credentials=supports_credentials)

# --- Register Blueprints ---
app.register_blueprint(auth_bp)
app.register_blueprint(patient_bp)
app.register_blueprint(org_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(trial_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(applications_bp)

# --- Register Global Error Handlers ---
register_error_handlers(app)

# --- Health check ---
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# --- Serve React Frontend (optional, for single-deploy mode) ---
# Enable by setting SERVE_FRONTEND=true and ensuring a build/ directory exists next to app.py
if os.getenv('SERVE_FRONTEND', 'false').lower() == 'true':
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

# --- Main Execution Block ---
if __name__ == '__main__':
    print("🚀 Starting Virtual Patient Recruitment API...")

    # Load ML models on startup
    loaded_count = load_models()
    print(f"✅ Loaded {loaded_count} models: {list(MODELS.keys())}")

    # Test database connection on startup
    conn = get_db_connection()
    if conn:
        print("✅ Database connection successful")
        conn.close()
    else:
        print("❌ Database connection failed")

    # Get port from environment variable for deployment platforms like Render/Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)