// src/components/Auth/ProtectedRoute.js

import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = ({ allowedRoles }) => {
  const isAuthenticated = localStorage.getItem("authToken");
  const role = localStorage.getItem("role");

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    // Redirect to the correct home based on role
    return <Navigate to={role === "admin" ? "/bulk-upload" : "/dashboard"} replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
