import React, { useEffect, useState } from 'react';
import { FaHistory, FaCheckCircle, FaTimesCircle, FaRocket } from 'react-icons/fa';
import apiService from '../../services/api';
import { Link } from 'react-router-dom';

const statusBadge = (eligibility) => {
  const ok = String(eligibility).toLowerCase() === 'eligible';
  return (
    <span className={`status-badge ${ok ? 'eligible' : 'ineligible'}`}>
      {ok ? <FaCheckCircle style={{ marginRight: 6 }} /> : <FaTimesCircle style={{ marginRight: 6 }} />}
      {eligibility}
    </span>
  );
};

const formatDate = (iso) => new Date(iso).toLocaleString();

const EmptyState = () => (
  <div className="content-wrapper" style={{ textAlign: 'center', padding: '3rem 1rem' }}>
    <div style={{ fontSize: 56, color: 'var(--primary-color)', marginBottom: 16 }}>
      <FaRocket />
    </div>
    <h2>No applications yet</h2>
    <p style={{ color: 'var(--gray-600)', maxWidth: 520, margin: '0 auto 1rem' }}>
      Start your journey by applying to a clinical trial. It only takes a few minutes and could
      help shape the future of healthcare.
    </p>
    <Link to="/patient-application" className="btn primary">Apply to a Trial</Link>
  </div>
);

const MyApplications = () => {
  const [loading, setLoading] = useState(true);
  const [items, setItems] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const res = await apiService.getMyApplications();
        setItems(res.data.applications || []);
      } catch (e) {
        setItems([]);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  if (loading) return <div className="content-wrapper">Loading...</div>;
  if (!items.length) return <EmptyState />;

  return (
    <div className="content-wrapper">
      <div className="dashboard-header">
        <h1><FaHistory style={{ marginRight: 8 }} /> My Applications</h1>
        <p>Your previous trial applications and eligibility status.</p>
      </div>

      <div className="patients-table-container">
        <table className="patients-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Trial</th>
              <th>Status</th>
              <th>Applied On</th>
            </tr>
          </thead>
          <tbody>
            {items.map((r, idx) => (
              <tr key={idx}>
                <td>{idx + 1}</td>
                <td>{r.trial_type}</td>
                <td>{statusBadge(r.eligibility)}</td>
                <td>{formatDate(r.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default MyApplications;