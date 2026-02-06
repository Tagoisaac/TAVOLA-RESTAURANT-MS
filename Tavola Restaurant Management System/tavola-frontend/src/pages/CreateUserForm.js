import React, { useState } from 'react';
import APIService from '../services/api';

const CreateUserForm = ({ onCreated, permissions = [] }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [roleId, setRoleId] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const payload = { username, email, password, full_name: fullName };
      if (roleId) payload.role_id = parseInt(roleId, 10);
      const user = await APIService.createUser(payload.username || username, payload.email || email, payload.password || password, payload.full_name || fullName);
      onCreated(user);
      setUsername(''); setEmail(''); setPassword(''); setFullName(''); setRoleId('');
    } catch (err) {
      setError(err.message || 'Failed to create user');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-user-form">
      {error && <div className="error-message">{error}</div>}
      <div className="form-row">
        <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} required />
        <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      </div>
      <div className="form-row">
        <input placeholder="Full name" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
        <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
      </div>
      <div className="form-row">
        <input placeholder="Role ID (optional)" value={roleId} onChange={(e) => setRoleId(e.target.value)} />
        <button type="submit" disabled={loading}>{loading ? 'Creating...' : 'Create User'}</button>
      </div>
    </form>
  );
};

export default CreateUserForm;
