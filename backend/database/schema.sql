-- Drop existing tables to ensure a clean slate, if they exist
DROP TABLE IF EXISTS hypertension_patients, arthritis_patients, migraine_patients, phase1_patients, users CASCADE;

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type VARCHAR(50) NOT NULL DEFAULT 'patient',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Hypertension patients table
CREATE TABLE IF NOT EXISTS hypertension_patients (
    id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    gender VARCHAR(10) NOT NULL,
    bmi DECIMAL(5,2) NOT NULL,
    glucose DECIMAL(6,2) NOT NULL,
    lifestyle_risk INT NOT NULL,
    stress_level INT NOT NULL,
    systolic_bp INT NOT NULL,
    diastolic_bp INT NOT NULL,
    cholesterol_total DECIMAL(6,2) NOT NULL,
    comorbidities INT NOT NULL,
    consent VARCHAR(5) NOT NULL,
    eligibility VARCHAR(20) NOT NULL,
    source VARCHAR(20) DEFAULT 'Patient',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Arthritis patients table
CREATE TABLE IF NOT EXISTS arthritis_patients (
    id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    years_since_diagnosis DECIMAL(4,1) NOT NULL,
    tender_joint_count INT NOT NULL,
    swollen_joint_count INT NOT NULL,
    crp_level DECIMAL(6,2) NOT NULL,
    patient_pain_score INT NOT NULL,
    egfr DECIMAL(6,2) NOT NULL,
    on_biologic_dmards INT NOT NULL,
    has_hepatitis INT NOT NULL,
    eligibility VARCHAR(20) NOT NULL,
    source VARCHAR(20) DEFAULT 'Patient',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Migraine patients table
CREATE TABLE IF NOT EXISTS migraine_patients (
    id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    migraine_frequency INT NOT NULL,
    previous_medication_failures INT NOT NULL,
    liver_enzyme_level DECIMAL(6,2) NOT NULL,
    has_aura INT NOT NULL,
    chronic_kidney_disease INT NOT NULL,
    on_anticoagulants INT NOT NULL,
    sleep_disorder INT NOT NULL,
    depression INT NOT NULL,
    caffeine_intake INT NOT NULL,
    eligibility VARCHAR(20) NOT NULL,
    source VARCHAR(20) DEFAULT 'Patient',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Phase 1 patients table
CREATE TABLE IF NOT EXISTS phase1_patients (
    id SERIAL PRIMARY KEY,
    age INT NOT NULL,
    sex INT NOT NULL,
    weight_kg DECIMAL(5,2) NOT NULL,
    height_cm DECIMAL(5,2) NOT NULL,
    bmi DECIMAL(5,2) NOT NULL,
    cohort INT NOT NULL,
    alt DECIMAL(6,2) NOT NULL,
    creatinine DECIMAL(5,2) NOT NULL,
    sbp INT NOT NULL,
    dbp INT NOT NULL,
    hr INT NOT NULL,
    temp_c DECIMAL(4,1) NOT NULL,
    adverse_event INT NOT NULL,
    eligibility VARCHAR(20) NOT NULL,
    source VARCHAR(20) DEFAULT 'Patient',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Applications audit table for linking submissions to users
CREATE TABLE IF NOT EXISTS applications (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL,
    trial_type VARCHAR(50) NOT NULL,
    patient_record_id INT NOT NULL,
    eligibility VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_applications_username ON applications(username);
CREATE INDEX IF NOT EXISTS idx_applications_created ON applications(created_at);

-- Insert default admin user with a Werkzeug-compatible password hash for 'admin'
INSERT INTO users (username, password_hash, user_type)
VALUES (
    'Admin',
    'scrypt:32768:8:1$3c53YnPmyLw0FlgX$47c110886a79bfaceb39b9af46baba2cc036ab23e1372c656a8c2bdb83fb4a3ba2c0cee7d7366d9bb7bcd81a6062f440d5da2d784fa4161e0d052826b2b0d801',
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_hypertension_created ON hypertension_patients(created_at);
CREATE INDEX IF NOT EXISTS idx_arthritis_created ON arthritis_patients(created_at);
CREATE INDEX IF NOT EXISTS idx_migraine_created ON migraine_patients(created_at);
CREATE INDEX IF NOT EXISTS idx_phase1_created ON phase1_patients(created_at);

