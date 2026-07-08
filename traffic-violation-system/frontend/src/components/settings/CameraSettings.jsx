import React from 'react';
import { Video } from 'lucide-react';

export default function CameraSettings({ settings, onChange }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <Video className="w-4 h-4 text-purple-400" />
        <span>Stream Tracking Configurations</span>
      </h3>

      <div className="space-y-1.5 text-xs">
        <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Reconnect interval (sec)</label>
        <input
          type="number"
          value={settings.camera_reconnect_interval_sec || 10}
          onChange={(e) => onChange('camera_reconnect_interval_sec', parseInt(e.target.value))}
          className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
        />
      </div>
    </div>
  );
}
