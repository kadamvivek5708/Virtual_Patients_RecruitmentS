# Virtual Patient Recruitment System

A full-stack web application for virtual clinical trial recruitment, patient eligibility screening, and analytics. The platform enables organizations to manage clinical trials, allows patients to apply for trials, and provides bulk upload and analytics features.

---

## Features

- **User Authentication**: Secure login and registration for users.
- **Patient Application**: Dynamic forms for patients to apply for clinical trials.
- **Bulk Upload**: Upload CSV/Excel files for bulk patient eligibility screening.
- **Analytics Dashboard**: Visualize trial applications, eligibility rates, and more.
- **Admin Dashboard**: Manage trials and view participant statistics.
- **Machine Learning Integration**: Automated eligibility screening using ML models.

---

## Project Structure
backend/
  app.py              # Flask app entry
  config.py           # Config settings
  requirements.txt    # Backend dependencies
  database/
    schema.sql        # DB schema
    setup_db.py       # DB setup script
  ml_models/          # Saved ML models (*.pkl)
  models/             # ML model utilities
  routes/             # API route handlers
  utils/              # Helper functions

frontend/
  package.json        # Dependencies
  public/index.html   # Entry HTML
  src/
    App.js            # Main React app
    index.js          # React entry
    components/       # UI components
    services/         # API calls
    styles/           # Global styles



Getting Started

### Backend

1. Navigate to the `backend/` directory:
    ```sh
    cd backend
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Set up the database:
    ```sh
    python database/setup_db.py
    ```
4. Run the Flask app:
    ```sh
    python app.py
    ```

### Frontend

1. Navigate to the `frontend/` directory:
    ```sh
    cd frontend
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Start the React app:
    ```sh
    npm start
    ```

### Usage
Login/Register: Access the app at /login or /register.
Dashboard: View welcome page and trial overview.
Patient Application: Apply for trials via dynamic forms.
Bulk Upload: Upload patient data for batch screening.
Analytics: View charts and statistics for all trials.

### Technologies Used
Frontend: React, React Router, CSS Modules, recharts, react-icons, react-hot-toast
Backend: Flask, SQLAlchemy, Python, scikit-learn (for ML models)
Database: SQLite (default, can be swapped)
Other: Axios (API calls), CSV/Excel parsing