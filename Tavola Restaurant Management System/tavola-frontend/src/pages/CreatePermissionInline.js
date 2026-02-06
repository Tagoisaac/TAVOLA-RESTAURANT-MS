import React, { useState } from 'react';
import APIService from '../services/api';

const CreatePermissionInline = ({ onCreated }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const p = await APIService.createPermission(name, description);
      onCreated(p);
      setName(''); setDescription('');
    } catch (err) {
      alert(err.message || 'Failed to create permission');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} style={{ marginBottom: 12 }}>
      <input placeholder="permission name" value={name} onChange={(e)=>setName(e.target.value)} required />
      <input placeholder="description" value={description} onChange={(e)=>setDescription(e.target.value)} style={{ marginLeft: 8 }} />
      <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>{loading ? 'Creating...' : 'Create'}</button>
    </form>
  );
};

export default CreatePermissionInline;
