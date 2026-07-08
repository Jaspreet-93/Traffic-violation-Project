import React, { useState, useEffect } from 'react';
import { officerEmailAPI } from '../../services/officerEmailApi';
import OfficerEmailTable from './OfficerEmailTable';
import OfficerEmailForm from './OfficerEmailForm';
import { Mail, CheckCircle, XCircle } from 'lucide-react';

export default function OfficerEmailManagement() {
  const [emails, setEmails] = useState([]);
  const [editItem, setEditItem] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState(null);

  const loadData = async () => {
    try {
      const res = await officerEmailAPI.getEmails();
      setEmails(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSave = async (payload) => {
    try {
      setMessage(null);
      if (editItem) {
        await officerEmailAPI.updateEmail(editItem.id, payload);
        setMessage({ type: 'success', text: 'Officer email updated successfully.' });
      } else {
        await officerEmailAPI.addEmail(payload);
        setMessage({ type: 'success', text: 'New officer email added successfully.' });
      }
      setEditItem(null);
      loadData();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this officer email recipient?')) return;
    try {
      setMessage(null);
      await officerEmailAPI.deleteEmail(id);
      setMessage({ type: 'success', text: 'Officer email recipient deleted.' });
      loadData();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleToggleStatus = async (id, active) => {
    try {
      setMessage(null);
      await officerEmailAPI.updateStatus(id, active);
      loadData();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  const handleSetPrimary = async (id) => {
    try {
      setMessage(null);
      await officerEmailAPI.setPrimary(id);
      loadData();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    }
  };

  if (loading) {
    return <div className="text-xs text-slate-550">Loading Recipient Registry...</div>;
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4 lg:col-span-2">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Mail className="w-4.5 h-4.5 text-purple-400" />
        <span>Officer Email Management</span>
      </h3>

      <p className="text-xs text-slate-500 font-semibold leading-relaxed">
        Manage the active list of official email destinations to receive traffic violation alerts and evidence.
      </p>

      {message && (
        <div className={`p-3 rounded-lg flex items-center space-x-2 text-xs font-semibold border ${
          message.type === 'success'
            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
            : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
        }`}>
          {message.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
          <span>{message.text}</span>
        </div>
      )}

      <OfficerEmailTable
        emails={emails}
        onEdit={setEditItem}
        onDelete={handleDelete}
        onToggleStatus={handleToggleStatus}
        onSetPrimary={handleSetPrimary}
      />

      <OfficerEmailForm
        editItem={editItem}
        onSave={handleSave}
        onCancel={() => setEditItem(null)}
      />
    </div>
  );
}
