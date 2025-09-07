// src/components/Layout/Layout.js

import React, { useState } from 'react';
import { useLocation, Outlet, useNavigate } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

const Layout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div className="layout">
      {/* Pass handleLogout down to Navbar */}
      <Navbar onMenuToggle={toggleSidebar} onLogout={handleLogout} />
      <div className="layout-content">
        <Sidebar 
          isOpen={sidebarOpen} 
          onClose={closeSidebar} 
          currentPath={location.pathname}
        />
        <main className={`main-content ${sidebarOpen ? '' : 'expanded'}`}>
          <div className="content-wrapper">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
