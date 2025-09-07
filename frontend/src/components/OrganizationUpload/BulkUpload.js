import React, { useState } from 'react';
import { 
  FaUpload, 
  FaFileAlt, 
  FaSpinner,
  FaCheckCircle,
  FaTimesCircle,
  FaDownload,
  FaHeartbeat,
  FaBone,
  FaBrain,
  FaVial
} from 'react-icons/fa';
import apiService from '../../services/api';
import toast from 'react-hot-toast';
import '../../styles/BulkUpload.css';

const BulkUpload = () => {
  const [selectedTrialType, setSelectedTrialType] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResults, setUploadResults] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const trialTypes = [
    {
      id: 'hypertension',
      name: 'Hypertension Clinical Trial',
      icon: FaHeartbeat
    },
    {
      id: 'arthritis',
      name: 'Arthritis Clinical Trial',
      icon: FaBone
    },
    {
      id: 'migraine',
      name: 'Migraine Clinical Trial',
      icon: FaBrain
    },
    {
      id: 'phase1',
      name: 'Phase 1 Clinical Trial',
    
      icon: FaVial
    }
  ];

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (file) => {
    const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const allowedExtensions = ['.csv', '.xls', '.xlsx'];
    
    const fileExtension = file.name.toLowerCase().substr(file.name.lastIndexOf('.'));
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      toast.error('Please select a CSV or Excel file');
      return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      toast.error('File size must be less than 10MB');
      return;
    }
    
    setSelectedFile(file);
    toast.success('File selected successfully');
  };

  const handleFileInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedTrialType) {
      toast.error('Please select a trial type');
      return;
    }
    
    if (!selectedFile) {
      toast.error('Please select a file to upload');
      return;
    }

    try {
      setUploading(true);
      
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('trial_type', selectedTrialType);
      
      const response = await apiService.uploadBulkFile(formData);
      setUploadResults(response.data);
      toast.success('File uploaded and processed successfully!');
      
    } catch (error) {
      console.error('Upload error:', error);
      toast.error(error.response?.data?.error || 'Failed to upload file');
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setSelectedTrialType('');
    setUploadResults(null);
    setDragActive(false);
  };

  const downloadTemplate = () => {
    const templates = {
      hypertension: 'age,gender,bmi,glucose,lifestyle_risk,stress_level,systolic_bp,diastolic_bp,cholesterol_total,comorbidities,consent\n45,Male,26.5,95,1,7,140,85,220,1,Yes',
      arthritis: 'age,years_since_diagnosis,tender_joint_count,swollen_joint_count,crp_level,patient_pain_score,egfr,on_biologic_dmards,has_hepatitis\n55,5.2,8,6,15.3,7,75.5,1,0',
      migraine: 'age,migraine_frequency,previous_medication_failures,liver_enzyme_level,has_aura,chronic_kidney_disease,on_anticoagulants,sleep_disorder,depression,caffeine_intake\n35,8,2,25.5,1,0,0,1,0,3',
      phase1: 'age,sex,weight_kg,height_cm,bmi,cohort,alt,creatinine,sbp,dbp,hr,temp_c,adverse_event\n28,0,70.5,175.0,23.0,1,22.3,0.9,120,80,72,36.5,0'
    };

    if (!selectedTrialType || !templates[selectedTrialType]) {
      toast.error('Please select a trial type first');
      return;
    }

    const csvContent = templates[selectedTrialType];
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${selectedTrialType}_template.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
    toast.success('Template downloaded successfully');
  };

  if (uploadResults) {
    return (
      <div className="bulk-upload fade-in">
        <div className="upload-results">
          <div className="results-header">
            <h2>Upload Results</h2>
            <button className="upload-btn" onClick={resetUpload}>
              Upload Another File
            </button>
          </div>

          <div className="results-summary">
            <div className="summary-card total">
              <div className="summary-number">{uploadResults.total_processed}</div>
              <div className="summary-label">Total Processed</div>
            </div>
            <div className="summary-card eligible">
              <div className="summary-number">{uploadResults.eligible}</div>
              <div className="summary-label">Eligible</div>
            </div>
            <div className="summary-card ineligible">
              <div className="summary-number">{uploadResults.ineligible}</div>
              <div className="summary-label">Ineligible</div>
            </div>
            <div className="summary-card errors">
              <div className="summary-number">{uploadResults.errors}</div>
              <div className="summary-label">Errors</div>
            </div>
          </div>

          {uploadResults.results && uploadResults.results.length > 0 && (
            <div className="detailed-results">
              <h3>Detailed Results (First 100 entries)</h3>
              <div className="results-table-container">
                <table className="results-table">
                  <thead>
                    <tr>
                      <th>Row</th>
                      <th>Patient ID</th>
                      <th>Eligibility</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {uploadResults.results.map((result, index) => (
                      <tr key={index}>
                        <td>{result.row}</td>
                        <td>{result.patient_id || 'N/A'}</td>
                        <td>
                          <span className={`eligibility-badge ${result.eligibility?.toLowerCase()}`}>
                            {result.eligibility === 'Eligible' && <FaCheckCircle />}
                            {result.eligibility === 'Ineligible' && <FaTimesCircle />}
                            {result.eligibility === 'Error' && <FaTimesCircle />}
                            {result.eligibility}
                          </span>
                        </td>
                        <td>
                          {result.error ? (
                            <span className="error-message">{result.error}</span>
                          ) : (
                            <span className="success-message">Processed</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="bulk-upload fade-in">
      <div className="upload-header">
        <h1>Bulk Patient Upload</h1>
        <p>Upload CSV or Excel files with patient data for eligibility screening</p>
      </div>

      <div className="upload-content">
        {/* Trial Type Selection */}
        <div className="trial-type-selector">
          <h3>Select Trial Type</h3>
          <div className="radio-group">
            {trialTypes.map((trial) => {
              const IconComponent = trial.icon;
              return (
                <label key={trial.id} className="radio-label">
                  <input
                    type="radio"
                    name="trialType"
                    value={trial.id}
                    checked={selectedTrialType === trial.id}
                    onChange={(e) => setSelectedTrialType(e.target.value)}
                  />
                  <IconComponent className="trial-icon" />
                  <div className="trial-info">
                    <span className="trial-name">{trial.name}</span>
                    <span className="trial-desc">{trial.description}</span>
                  </div>
                </label>
              );
            })}
          </div>
        </div>

        {/* Template Download */}
        {selectedTrialType && (
          <div className="template-section">
            <h3>Download Template</h3>
            <p>Download the CSV template for the selected trial type to ensure proper data format</p>
            <button className="upload-btn" onClick={downloadTemplate}>
              <FaDownload />
              Download {selectedTrialType} Template
            </button>
          </div>
        )}

        {/* File Upload */}
        <div className="file-uploader">
          <h3>Upload Patient Data</h3>
          <div
            className={`file-drop-zone ${dragActive ? 'active' : ''} ${!selectedTrialType ? 'disabled' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => selectedTrialType && document.getElementById('file-input').click()}
          >
            <input
              id="file-input"
              type="file"
              className="file-input"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileInputChange}
              disabled={!selectedTrialType}
            />
            
            {selectedFile ? (
              <div className="file-selected">
                <FaFileAlt className="file-icon" />
                <div className="file-info">
                  <p className="file-name">{selectedFile.name}</p>
                  <p className="file-size">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
                <button 
                  className="remove-file"
                  onClick={(e) => {
                    e.stopPropagation();
                    setSelectedFile(null);
                  }}
                >
                  <FaTimesCircle />
                </button>
              </div>
            ) : (
              <div className="drop-zone-content">
                <FaUpload className="upload-icon" />
                <h4>{selectedTrialType ? 'Drop your file here' : 'Select a trial type first'}</h4>
                <p>or click to browse</p>
                <small>Supports CSV, XLS, XLSX (max 10MB)</small>
              </div>
            )}
          </div>

          {selectedFile && selectedTrialType && (
            <div className="upload-actions">
              <button 
                className="upload-btn"
                onClick={handleUpload}
                disabled={uploading}
              >
                {uploading ? (
                  <>
                    <FaSpinner className="spinning" />
                    Processing File...
                  </>
                ) : (
                  <>
                    <FaUpload />
                    Upload and Process
                  </>
                )}
              </button>
            </div>
          )}
        </div>

        {/* Upload Instructions */}
        <div className="upload-instructions">
          <h3>Upload Instructions</h3>
          <div className="instructions-content">
            <div className="instruction-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h4>Select Trial Type</h4>
                <p>Choose the appropriate clinical trial type for your patient data</p>
              </div>
            </div>
            <div className="instruction-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h4>Download Template</h4>
                <p>Download and use the CSV template to ensure your data is formatted correctly</p>
              </div>
            </div>
            <div className="instruction-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h4>Upload File</h4>
                <p>Upload your CSV or Excel file with patient data for bulk eligibility screening</p>
              </div>
            </div>
            <div className="instruction-step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h4>Review Results</h4>
                <p>Review the eligibility results for each patient and download the processed data</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BulkUpload;