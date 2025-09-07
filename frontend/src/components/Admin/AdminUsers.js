import React, { useEffect, useState } from 'react';
import { FaUserClock } from 'react-icons/fa';
import apiService from '../../services/api';
import toast from 'react-hot-toast';

const formatDateTime = (iso) => {
  if (!iso) return '—';
  try {
    const d = new Date(iso);
    return d.toLocaleString(undefined, {
      year: 'numeric', month: 'short', day: '2-digit',
      hour: '2-digit', minute: '2-digit'
    });
  } catch {
    return iso;
  }
};

const AdminUsers = () => {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [role, setRole] = useState('patient');
  const [search, setSearch] = useState('');

  const fetchData = async (opts = {}) => {
    setLoading(true);
    try {
      const params = { role, search, page, pageSize, ...opts };
      const res = await apiService.getAdminUsers(params);
      setUsers(res.data.users || []);
      setTotal(res.data.total || 0);
      if (res.data.page) setPage(res.data.page);
      if (res.data.page_size) setPageSize(res.data.page_size);
    } catch (e) {
      toast.error('Failed to fetch users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [role, page, pageSize]);

  const onSearchSubmit = (e) => {
    e.preventDefault();
    setPage(1);
    fetchData({ page: 1 });
  };

  const onExportCsv = async () => {
    try {
      const res = await apiService.exportAdminUsersCsv({ role, search });
      const blob = new Blob([res.data], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'users.csv';
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      toast.error('CSV export failed');
    }
  };

  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  return (
    <div className="content-wrapper">
      <div className="dashboard-header">
        <h1><FaUserClock style={{ marginRight: 8 }} /> Users</h1>
        <p>Filter by role, search by username, paginate results, or export CSV.</p>
      </div>

      {/* Controls */}
      <form onSubmit={onSearchSubmit} style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <select value={role} onChange={(e) => { setRole(e.target.value); setPage(1); }} className="analytics form-select">
          <option value="patient">Patient</option>
          <option value="admin">Admin</option>
          <option value="all">All</option>
        </select>
        <input
          type="text"
          placeholder="Search username..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ padding: '0.5rem 0.75rem', border: '1px solid var(--gray-300)', borderRadius: 8, flex: 1 }}
        />
        <button className="btn primary" type="submit">Search</button>
        <button className="btn ghost" type="button" onClick={onExportCsv}>Export CSV</button>
      </form>

      <div className="patients-table-container">
        <table className="patients-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Role</th>
              <th>Created At</th>
              <th>Last Login</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr><td colSpan={5}>Loading...</td></tr>
            ) : users.length === 0 ? (
              <tr><td colSpan={5}>No users found.</td></tr>
            ) : (
              users.map((u, idx) => (
                <tr key={u.username + idx}>
                  <td>{(page - 1) * pageSize + idx + 1}</td>
                  <td>{u.username}</td>
                  <td>{u.user_type}</td>
                  <td>{formatDateTime(u.created_at)}</td>
                  <td>{formatDateTime(u.last_login)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        <div className="table-footer" style={{ display: 'flex', alignItems: 'center', gap: 8, justifyContent: 'space-between' }}>
          <div>Showing {(users.length ? (page - 1) * pageSize + 1 : 0)}–{(page - 1) * pageSize + users.length} of {total}</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <button className="btn ghost" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>Prev</button>
            <span>Page {page} / {totalPages}</span>
            <button className="btn ghost" disabled={page >= totalPages} onClick={() => setPage((p) => Math.min(totalPages, p + 1))}>Next</button>
            <select value={pageSize} onChange={(e) => { setPageSize(parseInt(e.target.value, 10)); setPage(1); }} className="analytics form-select">
              <option value={10}>10</option>
              <option value={20}>20</option>
              <option value={50}>50</option>
              <option value={100}>100</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminUsers;