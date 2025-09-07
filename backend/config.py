import os

# Configuration sourced from environment variables for production safety.
# DATABASE_URL takes precedence in utils/db.py. DB_CONFIG is a local fallback.
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'dbname': os.getenv('DB_NAME', 'virtual_patient_recruitment'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),  # set in .env (do not commit secrets)
    'port': int(os.getenv('DB_PORT', '5432'))
}

MODEL_PATHS = {
    'hypertension': 'ml_models/hypertension_model.pkl',
    'arthritis': 'ml_models/arthritis_model.pkl',
    'migraine': 'ml_models/migraine_model.pkl',
    'phase1': 'ml_models/phase1_model.pkl'
}

