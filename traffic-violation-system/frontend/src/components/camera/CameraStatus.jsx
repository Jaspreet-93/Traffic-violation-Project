import React from 'react';
import { Video, ShieldCheck, HelpCircle } from 'lucide-react';

export default function CameraStatus({ status }) {
  if (!status) return null;

  const cards = [
    { label: 'Total Connected', value: status.total_cameras, color: 'text-purple-400' },
    { label: 'Online Streams', value: status.online_cameras, color: 'text-emerald-450' },
    { label: 'Offline Streams', value: status.offline_cameras, color: 'text-rose-450' },
    { label: 'Recording Storage', value: status.recording_cameras, color: 'text-sky-400' }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((c, idx) => (
        <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4.5 shadow flex flex-col justify-between space-y-2">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">{c.label}</span>
          <span className={`text-xl font-bold font-mono ${c.color}`}>{c.value}</span>
        </div>
      ))}
    </div>
  );
}
