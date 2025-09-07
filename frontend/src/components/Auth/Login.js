// src/components/Auth/Login.js

import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaEnvelope, FaLock, FaEye, FaEyeSlash } from 'react-icons/fa';
import styles from './AuthForm.module.css';
import toast from 'react-hot-toast';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',   // backend expects username
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    // Prefill username if remembered
    const remembered = localStorage.getItem('rememberedUsername');
    if (remembered) {
      setFormData((prev) => ({ ...prev, username: remembered }));
      setRememberMe(true);
    }
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/login', formData);

      if (response.status === 200) {
        const { user_type, role: roleFromBackend, username } = response.data;
        const role = roleFromBackend || user_type;

        // Save auth info
        localStorage.setItem('authToken', 'dummy-token'); // replace with real token when available
        localStorage.setItem('role', role);
        localStorage.setItem('username', username);

        if (rememberMe) {
          localStorage.setItem('rememberedUsername', formData.username);
        } else {
          localStorage.removeItem('rememberedUsername');
        }

        toast.success('Login successful!');

        // Redirect based on role
        if (role === 'admin') {
          navigate('/bulk-upload');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (error) {
      console.error('Login error:', error);
      const msg = error.response?.data?.error || 'Login failed. Try again.';
      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={`${styles.authCard} ${styles.fadeIn}`}>
        <h2 className={styles.title}>Welcome Back</h2>
        <p className={styles.subtitle}>Please enter your credentials to log in.</p>
        
        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <FaEnvelope className={styles.inputIcon} />
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
              autoComplete="username"
            />
          </div>

          <div className={styles.inputGroup}>
            <FaLock className={styles.inputIcon} />
            <input
              type={showPassword ? 'text' : 'password'}
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              autoComplete="current-password"
            />
            <button
              type="button"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
              className={styles.passwordToggle}
              onClick={() => setShowPassword((s) => !s)}
              tabIndex={0}
            >
              {showPassword ? <FaEyeSlash /> : <FaEye />}
            </button>
          </div>

          <div className={styles.formRow}>
            <label className={styles.checkboxLabel}>
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
              />
              Remember me
            </label>
          </div>

          <button type="submit" className={styles.submitButton} disabled={loading}>
            {loading ? <span className={styles.btnSpinner} /> : 'Log In'}
          </button>
        </form>

        <p className={styles.redirectText}>
          Don't have an account? <Link to="/register">Sign Up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
