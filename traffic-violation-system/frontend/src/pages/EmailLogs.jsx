import React, { useState, useEffect } from 'react';
import { emailAPI } from '../services/emailApi';
import EmailLogTable from '../components/email/EmailLogTable';
import SendTestEmail from '../components/email/SendTestEmail';

export default function EmailLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const res = await emailAPI.getLogs();
      setLogs(res.data);
    } catch (err) {
      console.error("Failed to load email logs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [refreshKey]);

  const handleRefresh = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Email Notification Logs</h2>
          <p className="text-xs text-slate-500">Track and audit the delivery status of automated traffic violation alert dispatches.</p>
        </div>
        <button
          onClick={handleRefresh}
          className="text-xs font-semibold px-4 py-2 border border-slate-800 bg-slate-900 rounded-lg hover:bg-slate-850 text-slate-300 transition-colors"
        >
          Refresh Logs
        </button>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Logs Table (2 cols) */}
        <div className="lg:col-span-2">
          <EmailLogTable logs={logs} loading={loading} />
        </div>

        {/* Sidebar Test dispatch (1 col) */}
        <div>
          <SendTestEmail onSendSuccess={handleRefresh} />
        </div>
      </div>
    </div>
  );
}
