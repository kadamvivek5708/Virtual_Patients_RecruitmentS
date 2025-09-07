import React, { useState, useEffect } from 'react';
import { 
  FaHeartbeat, 
  FaBone, 
  FaBrain, 
  FaVial, 
  FaArrowLeft, 
  FaSpinner,
  FaCheckCircle,
  FaTimesCircle
} from 'react-icons/fa';
import apiService from '../../services/api';
import toast from 'react-hot-toast';

const PatientApplication = () => {
  const [selectedTrial, setSelectedTrial] = useState(null);
  const [formFields, setFormFields] = useState([]);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  const trialTypes = [
    {
      id: 'hypertension',
      name: 'Hypertension Trial',
      description: 'Clinical trial for hypertension treatment and blood pressure management',
      icon: FaHeartbeat,
      color: 'red'
    },
    {
      id: 'arthritis',
      name: 'Arthritis Trial', 
      description: 'Rheumatoid arthritis treatment study with new therapeutic approaches',
      icon: FaBone,
      color: 'orange'
    },
    {
      id: 'migraine',
      name: 'Migraine Trial',
      description: 'Migraine prevention medication trial for chronic sufferers',
      icon: FaBrain,
      color: 'purple'
    },
    {
      id: 'phase1',
      name: 'Phase 1 Trial',
      description: 'Phase 1 safety and dosage study for new investigational drugs',
      icon: FaVial,
      color: 'blue'
    }
  ];

  useEffect(() => {
    if (selectedTrial) {
      fetchFormFields();
    }
  }, [selectedTrial]);

  const fetchFormFields = async () => {
    try {
      setLoading(true);
      const response = await apiService.getTrialFields(selectedTrial);
      setFormFields(response.data);
      
      // Initialize form data with default values
      const initialData = {};
      response.data.forEach(field => {
        if (field.options && field.options.length > 0) {
          // For select fields, don't set a default to force user selection
          initialData[field.name] = '';
        } else {
          initialData[field.name] = '';
        }
      });
      setFormData(initialData);
    } catch (error) {
      console.error('Error fetching form fields:', error);
      toast.error('Failed to load form fields');
    } finally {
      setLoading(false);
    }
  };

  const handleTrialSelect = (trialId) => {
    setSelectedTrial(trialId);
    setFormData({});
    setResult(null);
  };

  const handleInputChange = (fieldName, value) => {
    setFormData(prev => ({
      ...prev,
      [fieldName]: value
    }));
  };

  const validateForm = () => {
    const requiredFields = formFields.filter(field => field.required);
    const missingFields = [];
    const rangeErrors = [];

    requiredFields.forEach(field => {
      const value = formData[field.name];
      if (value === '' || value === null || value === undefined) {
        missingFields.push(field.label);
        return;
      }

      // Range checks for numeric fields
      if (field.type === 'number') {
        const num = Number(value);
        if (Number.isNaN(num)) {
          rangeErrors.push(`${field.label} must be a number`);
          return;
        }
        if (field.min !== undefined && num < field.min) {
          rangeErrors.push(`${field.label} must be >= ${field.min}`);
        }
        if (field.max !== undefined && num > field.max) {
          rangeErrors.push(`${field.label} must be <= ${field.max}`);
        }
      }
    });

    if (missingFields.length > 0) {
      toast.error(`Please fill in required fields: ${missingFields.join(', ')}`);
      return false;
    }

    if (rangeErrors.length > 0) {
      toast.error(rangeErrors[0]); // show the first error to guide user
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      setSubmitting(true);
      
      // Convert form data to appropriate types
      const processedData = {};
      formFields.forEach(field => {
        let value = formData[field.name];
        
        if (field.type === 'number') {
          value = parseFloat(value) || 0;
        } else if (field.type === 'select' && field.options) {
          // For select fields with value/label options, use the value
          const option = field.options.find(opt => opt.value == value || opt.label === value);
          if (option && typeof option === 'object' && 'value' in option) {
            value = option.value;
          }
        }
        
        processedData[field.name] = value;
      });

      const response = await apiService.submitPatientApplication({
        trial_type: selectedTrial,
        patient_data: processedData
      });

      setResult(response.data);
      toast.success('Application submitted successfully!');
      
    } catch (error) {
      console.error('Error submitting application:', error);
      toast.error(error.response?.data?.error || 'Failed to submit application');
    } finally {
      setSubmitting(false);
    }
  };

  const renderFormField = (field) => {
    const value = formData[field.name] || '';

    if (field.type === 'select') {
      return (
        <select
          className="form-select"
          value={value}
          onChange={(e) => handleInputChange(field.name, e.target.value)}
          required={field.required}
        >
          <option value="">Select {field.label}</option>
          {field.options.map((option, index) => (
            <option 
              key={index} 
              value={typeof option === 'object' ? option.value : option}
            >
              {typeof option === 'object' ? option.label : option}
            </option>
          ))}
        </select>
      );
    }

    return (
      <input
        type={field.type}
        className="form-input"
        value={value}
        onChange={(e) => handleInputChange(field.name, e.target.value)}
        min={field.min}
        max={field.max}
        step={field.step}
        required={field.required}
        placeholder={`Enter ${field.label.toLowerCase()}`}
      />
    );
  };

  const resetApplication = () => {
    setSelectedTrial(null);
    setFormData({});
    setResult(null);
    setFormFields([]);
  };

  if (result) {
    const isEligible = result.eligibility === 'Eligible';
    return (
      <div className="content-wrapper" style={{ textAlign: 'center' }}>
        <div style={{ maxWidth: 720, margin: '0 auto' }}>
          <div style={{
            padding: '2rem',
            borderRadius: '16px',
            border: `1px solid ${isEligible ? 'rgba(16,185,129,0.25)' : 'rgba(239,68,68,0.25)'}`,
            background: isEligible ? 'linear-gradient(180deg, #ecfdf5 0%, #ffffff 100%)' : 'linear-gradient(180deg, #fef2f2 0%, #ffffff 100%)',
            boxShadow: '0 10px 20px rgba(0,0,0,0.06)'
          }}>
            <div style={{ fontSize: 64, marginBottom: 12, color: isEligible ? 'var(--success-color)' : 'var(--danger-color)' }}>
              {isEligible ? <FaCheckCircle /> : <FaTimesCircle />}
            </div>
            <h2 style={{ fontSize: '1.75rem', marginBottom: 8 }}>Application Result</h2>
            <div style={{ marginBottom: 12 }}>
              <span className={`status-badge ${isEligible ? 'eligible' : 'ineligible'}`}>{result.eligibility}</span>
            </div>
            <p style={{ color: 'var(--gray-700)', marginBottom: 16 }}>{result.message}</p>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 12, textAlign: 'left', margin: '1rem 0 1.5rem' }}>
              <div style={{ padding: '0.75rem 1rem', borderRadius: 10, background: 'var(--gray-50)', border: '1px solid var(--gray-200)' }}>
                <div style={{ color: 'var(--gray-500)', fontSize: 12, textTransform: 'uppercase' }}>Patient ID</div>
                <div style={{ fontWeight: 700 }}>#{result.patient_id}</div>
              </div>
              <div style={{ padding: '0.75rem 1rem', borderRadius: 10, background: 'var(--gray-50)', border: '1px solid var(--gray-200)' }}>
                <div style={{ color: 'var(--gray-500)', fontSize: 12, textTransform: 'uppercase' }}>Trial Type</div>
                <div style={{ fontWeight: 700 }}>{result.trial_type}</div>
              </div>
              <div style={{ padding: '0.75rem 1rem', borderRadius: 10, background: 'var(--gray-50)', border: '1px solid var(--gray-200)' }}>
                <div style={{ color: 'var(--gray-500)', fontSize: 12, textTransform: 'uppercase' }}>Applied On</div>
                <div style={{ fontWeight: 700 }}>{new Date().toLocaleString()}</div>
              </div>
            </div>

            {isEligible ? (
              <div style={{
                background: '#ecfdf5',
                border: '1px solid rgba(16,185,129,0.25)',
                color: '#065f46',
                borderRadius: 12,
                padding: '1rem',
                marginBottom: '1rem'
              }}>
                Great news! You are eligible. Our research team will contact you in 2–3 business days with next steps.
              </div>
            ) : (
              <div style={{
                background: '#fef2f2',
                border: '1px solid rgba(239,68,68,0.25)',
                color: '#7f1d1d',
                borderRadius: 12,
                padding: '1rem',
                marginBottom: '1rem'
              }}>
                You’re not eligible for this trial based on the current information. You can try another trial.
              </div>
            )}

            <div style={{ display: 'flex', gap: 8, justifyContent: 'center' }}>
              <button className="btn primary" onClick={resetApplication}>
                Try Another Trial
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!selectedTrial) {
    return (
      <div className="patient-application fade-in">
        <div className="application-header">
          <h1>Patient Application</h1>
          <p>Select a clinical trial to check your eligibility and apply for participation</p>
        </div>

        <div className="trial-selector">
          <h2>Available Clinical Trials</h2>
          <div className="trials-grid">
            {trialTypes.map((trial) => {
              const IconComponent = trial.icon;
              return (
                <div 
                  key={trial.id} 
                  className={`trial-card clickable ${trial.color}`}
                  onClick={() => handleTrialSelect(trial.id)}
                >
                  <div className="trial-icon">
                    <IconComponent />
                  </div>
                  <h3>{trial.name}</h3>
                  <p>{trial.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="patient-application fade-in">
      <div className="dynamic-form">
        <div className="form-header">
          <button className="back-btn" onClick={() => setSelectedTrial(null)}>
            <FaArrowLeft />
            Back to Trials
          </button>
          <h2>{trialTypes.find(t => t.id === selectedTrial)?.name} Application</h2>
        </div>

        {loading ? (
          <div className="loading-spinner">
            <div className="spinner"></div>
          </div>
        ) : (
          <form className="patient-form" onSubmit={handleSubmit}>
            <div className="form-grid">
              {formFields.map((field, index) => (
                <div key={index} className="form-field">
                  <label className="form-label">
                    {field.label}
                    {field.required && <span className="required">*</span>}
                  </label>
                  {renderFormField(field)}
                  {field.min !== undefined && field.max !== undefined && (
                    <small className="field-hint">
                      Range: {field.min} - {field.max}
                    </small>
                  )}
                </div>
              ))}
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="submit-btn"
                disabled={submitting}
              >
                {submitting ? (
                  <>
                    <FaSpinner className="spinning" />
                    Submitting Application...
                  </>
                ) : (
                  'Submit Application'
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default PatientApplication;
