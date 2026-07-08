import React from 'react';
import { Video, Activity, RefreshCw, Trash2 } from 'lucide-react';

export default function CameraCard({ item, onToggle, onDelete, isActive, onSelect }) {
  return (
    <div 
      onClick={() => onSelect(item.id)}
      className={`bg-slate-900 border rounded-xl p-5 shadow flex flex-col justify-between space-y-4 transition-all cursor-pointer ${
        isActive ? 'border-purple-650 ring-1 ring-purple-650/40' : 'border-slate-800 hover:border-slate-700'
      }`}
    >
      <div className="flex justify-between items-start">
        <div className="space-y-1">
          <h4 className="text-xs font-bold text-slate-200">{item.name}</h4>
          <span className="text-[10px] text-slate-500 font-mono block truncate max-w-[200px]">{item.url}</span>
        </div>
        <span className={`px-2 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider ${
          item.status === 'Online' ? 'bg-emerald-500/10 text-emerald-450 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-450 border border-rose-500/20'
        }`}>
          {item.status}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-450 border-t border-b border-slate-850 py-2.5 font-semibold">
        <div>Resolution: <span className="text-slate-300 font-mono">{item.resolution}</span></div>
        <div>FPS: <span className="text-slate-300 font-mono">{item.fps}</span></div>
        <div>Health: <span className="text-slate-300">{item.health}</span></div>
        <div>Rec: <span className="text-slate-300">{item.recording_enabled ? "Active" : "Disabled"}</span></div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={(e) => { e.stopPropagation(); onToggle(item.id, !item.recording_enabled); }}
          className={`flex-1 font-semibold py-1.5 rounded text-[10px] flex items-center justify-center space-x-1 transition-all cursor-pointer ${
            item.recording_enabled ? 'bg-purple-650 text-white' : 'bg-slate-950 border border-slate-850 text-slate-450 hover:text-slate-200'
          }`}
        >
          <Activity className="w-3.5 h-3.5" />
          <span>{item.recording_enabled ? 'Rec: Active' : 'Enable Rec'}</span>
        </button>
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(item.id); }}
          className="p-1.5 rounded bg-slate-950 border border-slate-850 hover:bg-rose-500/10 text-slate-400 hover:text-rose-500 transition-all cursor-pointer"
          title="Remove device"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
