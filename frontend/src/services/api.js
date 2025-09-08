import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || window.location.origin;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes for file upload
});

// Request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`🔄 Making ${config.method?.toUpperCase()} request to: ${config.url}`);
    console.log('📤 Request data:', config.data);
    return config;
  },
  (error) => {
    console.error('❌ Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log(`✅ Response received:`, response.status);
    console.log('📥 Response data:', response.data);
    return response;
  },
  (error) => {
    console.error('❌ Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Health check
  healthCheck: () => api.get('/api'),
  
  // Get available trials
  getTrials: () => api.get('/api/trials'),
  
  // Get form fields for specific trial type
  getTrialFields: (trialType) => api.get(`/api/trial-fields/${trialType}`),
  
  // Submit patient application (sends username header if present)
  submitPatientApplication: (data) => {
    const username = localStorage.getItem('username');
    return api.post('/api/patient/apply', data, { headers: username ? { 'X-Username': username } : {} });
  },
  
  // Upload bulk file for organization
  uploadBulkFile: (formData) => {
    console.log('📤 Uploading file with form data:', formData);
    return api.post('/api/organization/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 120000, // 2 minutes for file upload
    });
  },
  
  // Get analytics data
  getAnalytics: () => api.get('/api/analytics'),
  
  // Get patients by trial type
  getPatients: (trialType) => api.get(`/api/patients/${trialType}`),

  // Patient applications history
  getMyApplications: () => {
    const username = localStorage.getItem('username');
    return api.get('/api/applications/me', { headers: username ? { 'X-Username': username } : {} });
  },

  // Admin - list users with filters/pagination
  getAdminUsers: ({ role = 'patient', search = '', page = 1, pageSize = 20 } = {}) =>
    api.get('/api/admin/users', { params: { role, search, page, page_size: pageSize } }),

  // Admin - export CSV (using same filters, no pagination)
  exportAdminUsersCsv: ({ role = 'patient', search = '' } = {}) =>
    api.get('/api/admin/users', { params: { role, search, export: 'csv' }, responseType: 'blob' }),
};

export default apiService;
