import React from 'react';
import { Folder } from 'lucide-react';

export default function StorageSettings({ settings, onChange }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <Folder className="w-4 h-4 text-purple-400" />
        <span>Evidence Disk Allocation</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Retention */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Storage retention period (days)</label>
          <input
            type="number"
            value={settings.recording_retention_days || 30}
            onChange={(e) => onChange('recording_retention_days', parseInt(e.target.value))}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>

        {/* Storage Location */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Physical Storage Path</label>
          <input
            type="text"
            value={settings.storage_location || './evidence'}
            onChange={(e) => onChange('storage_location', e.target.value)}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>
      </div>
    </div>
  );
}
