import React from 'react';
import { Mail, CheckCircle2, AlertCircle, HelpCircle } from 'lucide-react';

export default function EmailLogTable({ logs, loading }) {
  const formatTime = (timeStr) => {
    if (!timeStr) return 'N/A';
    try {
      const d = new Date(timeStr);
      return d.toLocaleString();
    } catch {
      return timeStr;
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-500 text-xs">
        <span className="w-5 h-5 rounded-full border-2 border-purple-500 border-t-transparent animate-spin mb-3"></span>
        <span>Loading dispatch logs...</span>
      </div>
    );
  }

  if (!logs || logs.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-655 text-xs bg-slate-900 border border-slate-800 rounded-xl">
        <Mail className="w-10 h-10 text-slate-800 mb-3" />
        <h4 className="font-semibold text-slate-400">No Email Logs Found</h4>
        <p className="text-[10px] text-slate-600 mt-1">Automated dispatch alerts will log history entries here.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/60 border-b border-slate-800 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4 w-16">Log ID</th>
              <th className="p-4 w-24">Violation ID</th>
              <th className="p-4">Recipient</th>
              <th className="p-4">Subject</th>
              <th className="p-4 w-28">Status</th>
              <th className="p-4 w-44">Sent At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-slate-955 transition-colors text-slate-300">
                <td className="p-4 font-mono font-bold text-slate-400">#{log.id}</td>
                <td className="p-4 font-mono font-semibold text-purple-400">#{log.violation_id}</td>
                <td className="p-4 text-slate-200 font-medium">{log.recipient_email}</td>
                <td className="p-4 max-w-xs truncate text-slate-400">{log.subject}</td>
                <td className="p-4">
                  {log.status === 'SENT' ? (
                    <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded text-emerald-450 text-[10px] font-bold uppercase w-fit">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Sent</span>
                    </div>
                  ) : log.status === 'FAILED' ? (
                    <div
                      title={log.error_message || "Delivery failed"}
                      className="flex items-center space-x-1.5 bg-rose-500/10 border border-rose-500/20 px-2 py-0.5 rounded text-rose-450 text-[10px] font-bold uppercase w-fit cursor-help"
                    >
                      <AlertCircle className="w-3 h-3" />
                      <span>Failed</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded text-amber-450 text-[10px] font-bold uppercase w-fit">
                      <HelpCircle className="w-3 h-3" />
                      <span>Pending</span>
                    </div>
                  )}
                </td>
                <td className="p-4 text-slate-500 font-mono text-[10px]">{formatTime(log.sent_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
