import React, { useState, useEffect } from 'react';
import { emailAPI } from '../../services/emailApi';
import { Settings, Save, CheckCircle, XCircle } from 'lucide-react';

export default function EmailSettings({ onStatusChange }) {
  const [stationName, setStationName] = useState('');
  const [stationEmail, setStationEmail] = useState('');
  const [smtpEmail, setSmtpEmail] = useState('');
  const [smtpPassword, setSmtpPassword] = useState('');
  const [enabled, setEnabled] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    async function loadSettings() {
      try {
        const res = await emailAPI.getSettings();
        setStationName(res.data.station_name || '');
        setStationEmail(res.data.station_email || '');
        setSmtpEmail(res.data.smtp_email || '');
        setSmtpPassword(res.data.smtp_password || '');
        setEnabled(res.data.enabled !== false);
      } catch (err) {
        console.error("Failed to load email configurations:", err);
      }
    }
    loadSettings();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      setMessage(null);
      await emailAPI.updateSettings({
        station_name: stationName,
        station_email: stationEmail,
        smtp_email: smtpEmail,
        smtp_password: smtpPassword,
        enabled: enabled
      });
      setMessage({ type: 'success', text: 'Configurations updated successfully.' });
      if (onStatusChange) onStatusChange();
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || err.message });
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Settings className="w-4.5 h-4.5 text-purple-400" />
        <span>Station SMTP Settings</span>
      </h3>

      <form onSubmit={handleSave} className="space-y-4">
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

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Station Name</label>
            <input
              type="text"
              value={stationName}
              onChange={(e) => setStationName(e.target.value)}
              placeholder="Central Police Station"
              required
              className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Station Email</label>
            <input
              type="email"
              value={stationEmail}
              onChange={(e) => setStationEmail(e.target.value)}
              placeholder="station@traffic.gov"
              required
              className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">SMTP Email Username</label>
            <input
              type="text"
              value={smtpEmail}
              onChange={(e) => setSmtpEmail(e.target.value)}
              placeholder="example@gmail.com"
              required
              className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">SMTP App Password</label>
            <input
              type="password"
              value={smtpPassword}
              onChange={(e) => setSmtpPassword(e.target.value)}
              placeholder="••••••••••••••••"
              required
              className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center space-x-3 py-2">
          <button
            type="button"
            onClick={() => setEnabled(!enabled)}
            className={`w-10 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-300 focus:outline-none ${
              enabled ? 'bg-purple-650' : 'bg-slate-800'
            }`}
          >
            <div className={`bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ${enabled ? 'translate-x-4' : 'translate-x-0'}`}></div>
          </button>
          <span className="text-xs text-slate-350">
            {enabled ? 'Email Notifications Enabled' : 'Email Notifications Disabled'}
          </span>
        </div>

        <button
          type="submit"
          disabled={saving}
          className="w-full bg-purple-650 hover:bg-purple-750 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs flex items-center justify-center space-x-2"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save Configuration'}</span>
        </button>
      </form>
    </div>
  );
}
