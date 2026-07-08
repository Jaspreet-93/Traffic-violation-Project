import React from 'react';
import { Mail } from 'lucide-react';

export default function SMTPSettings({ settings, onChange }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <Mail className="w-4 h-4 text-purple-400" />
        <span>SMTP Configuration</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Host */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">SMTP Server Host</label>
          <input
            type="text"
            value={settings.smtp_host || ''}
            onChange={(e) => onChange('smtp_host', e.target.value)}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>

        {/* Port */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">SMTP Server Port</label>
          <input
            type="number"
            value={settings.smtp_port || 587}
            onChange={(e) => onChange('smtp_port', parseInt(e.target.value))}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>
      </div>
    </div>
  );
}
