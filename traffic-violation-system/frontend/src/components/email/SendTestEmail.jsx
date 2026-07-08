import React, { useState } from 'react';
import { emailAPI } from '../../services/emailApi';
import { Send, CheckCircle, XCircle } from 'lucide-react';

export default function SendTestEmail({ onSendSuccess }) {
  const [recipient, setRecipient] = useState('');
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!recipient) return;

    try {
      setLoading(true);
      setMsg(null);
      const res = await emailAPI.sendTestEmail(recipient);
      setMsg({ type: 'success', text: res.data.message });
      setRecipient('');
      if (onSendSuccess) onSendSuccess();
    } catch (err) {
      setMsg({ type: 'error', text: err.response?.data?.detail || err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
      <h3 className="font-semibold text-sm text-slate-200 mb-3 flex items-center space-x-2">
        <Send className="w-4 h-4 text-purple-400" />
        <span>Dispatch Test Email</span>
      </h3>

      <form onSubmit={handleSend} className="space-y-3">
        {msg && (
          <div className={`p-3 rounded-lg flex items-center space-x-2 text-xs font-semibold border ${
            msg.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
          }`}>
            {msg.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
            <span className="truncate max-w-full">{msg.text}</span>
          </div>
        )}

        <div className="flex gap-2">
          <input
            type="email"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
            placeholder="officer@traffic.gov"
            required
            className="flex-1 bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-purple-650 hover:bg-purple-750 disabled:opacity-50 text-white font-semibold px-4 py-2 rounded-xl text-xs flex items-center space-x-1.5 shadow transition-all cursor-pointer"
          >
            <Send className="w-3.5 h-3.5" />
            <span>{loading ? 'Sending...' : 'Send'}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
