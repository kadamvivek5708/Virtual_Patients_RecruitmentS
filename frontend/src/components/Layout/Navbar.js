// src/components/Layout/Navbar.js

import React from 'react';
import { FaBars, FaFlask, FaUser, FaSignOutAlt } from 'react-icons/fa';

const Navbar = ({ onMenuToggle, onLogout }) => {
  const username = localStorage.getItem("username") || "Guest";
  const role = localStorage.getItem("role") || "";

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button className="menu-toggle" onClick={onMenuToggle}>
          <FaBars />
        </button>
        <div className="navbar-brand">
          <div className="brand-icon">
            <FaFlask />
          </div>
          <span className="brand-text">Virtual Patient Recruitment</span>
        </div>
      </div>
      
      <div className="navbar-actions">
        {/* User info */}
        <div className="nav-user">
          <FaUser className="user-icon" />
          <span>{username} {role && `(${role})`}</span>
        </div>

        {/* Logout */}
        <button className="nav-btn logout-btn" onClick={onLogout}>
          <FaSignOutAlt />
          <span>Logout</span>
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
