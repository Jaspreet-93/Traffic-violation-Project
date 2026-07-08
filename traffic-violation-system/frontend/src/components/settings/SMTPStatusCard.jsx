import React, { useState, useEffect } from 'react';
import { emailAPI } from '../../services/emailApi';
import { Shield, ShieldAlert, Activity, RefreshCw } from 'lucide-react';

export default function SMTPStatusCard({ refreshTrigger }) {
  const [loading, setLoading] = useState(false);
  const [statusData, setStatusData] = useState(null);

  const fetchStatus = async () => {
    try {
      setLoading(true);
      const res = await emailAPI.getStatus();
      setStatusData(res.data);
    } catch (err) {
      console.error("Failed to fetch SMTP server connection status:", err);
      setStatusData({ connected: false, enabled: false });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, [refreshTrigger]);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-full justify-between">
      <div>
        <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
          <Activity className="w-4.5 h-4.5 text-purple-400 animate-pulse" />
          <span>SMTP Connection Status</span>
        </h3>

        <div className="space-y-4">
          {/* Badge Display */}
          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-500">Service Status</span>
            {statusData?.connected ? (
              <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-emerald-450 text-[10px] font-bold uppercase">
                <Shield className="w-3.5 h-3.5" />
                <span>Connected</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1.5 bg-rose-500/10 border border-rose-500/20 px-3 py-1 rounded-full text-rose-450 text-[10px] font-bold uppercase animate-pulse">
                <ShieldAlert className="w-3.5 h-3.5" />
                <span>Disconnected</span>
              </div>
            )}
          </div>

          {/* Settings info block */}
          <div className="bg-slate-950 border border-slate-850 p-4 rounded-xl space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-550">Station Email Destination</span>
              <span className="text-slate-300 font-medium truncate max-w-[180px]">
                {statusData?.station_email || 'Not configured'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-550">SMTP Port</span>
              <span className="text-slate-300 font-medium">587 (STARTTLS)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-550">SMTP Host</span>
              <span className="text-slate-300 font-medium">smtp.gmail.com</span>
            </div>
          </div>
        </div>
      </div>

      <button
        onClick={fetchStatus}
        disabled={loading}
        className="w-full bg-slate-950 hover:bg-slate-950/80 border border-slate-800 disabled:opacity-50 font-semibold py-2 rounded-xl transition-all text-xs flex items-center justify-center space-x-1.5 mt-6 cursor-pointer text-slate-300"
      >
        <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
        <span>{loading ? 'Testing...' : 'Test Connection'}</span>
      </button>
    </div>
  );
}
