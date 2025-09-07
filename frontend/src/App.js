// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// --- Layouts and Authentication ---
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// --- Page Components ---
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import PatientApplication from './components/PatientForm/PatientApplication';
import MyApplications from './components/Patient/MyApplications';
import BulkUpload from './components/OrganizationUpload/BulkUpload';
import Analytics from './components/Analytics/Analytics';
import AdminUsers from './components/Admin/AdminUsers';
import Landing from './components/Landing/Landing';

// --- Global Styles ---
import './styles/App.css';

function App() {
  return (
    <>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<React.Suspense fallback={null}> <Landing /> </React.Suspense>} />

          {/* Protected Routes with role-based access */}
          <Route element={<ProtectedRoute allowedRoles={['patient', 'admin']} />}>
            <Route element={<Layout />}>
              {/* Patient Routes */}
              <Route element={<ProtectedRoute allowedRoles={['patient']} />}>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/patient-application" element={<PatientApplication />} />
                <Route path="/my-applications" element={<React.Suspense fallback={null}> <MyApplications /> </React.Suspense>} />
                 
              </Route>

              {/* Admin Routes */}
              <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
                <Route path="/bulk-upload" element={<BulkUpload />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/admin/users" element={<React.Suspense fallback={null}> <AdminUsers /> </React.Suspense>} />
              </Route>
            </Route>
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
      
      {/* Toast notifications */}
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
          },
        }}
      />
    </>
  );
}

export default App;
