import React from 'react';
import { Activity, ShieldCheck } from 'lucide-react';

export default function ModelHealthCard({ health }) {
  if (!health) return null;

  const colorMap = {
    Excellent: 'text-emerald-450 bg-emerald-500/5 border-emerald-500/10',
    Good: 'text-sky-400 bg-sky-500/5 border-sky-500/10',
    Warning: 'text-amber-450 bg-amber-500/5 border-amber-500/10',
    Critical: 'text-rose-450 bg-rose-500/5 border-rose-500/10'
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow flex flex-col justify-between space-y-4">
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-slate-200 flex items-center space-x-1.5">
          <Activity className="w-4 h-4 text-purple-400" />
          <span>Model Load Health</span>
        </h3>
        <span className={`px-2.5 py-0.5 rounded border text-[9px] font-bold uppercase tracking-wider ${colorMap[health.status] || 'text-slate-400'}`}>
          {health.status}
        </span>
      </div>

      <div className="space-y-3.5 text-xs font-semibold">
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Validation Status</span>
          <span className="text-emerald-450 flex items-center space-x-1"><ShieldCheck className="w-3.5 h-3.5" /> <span>Weights Loaded</span></span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">In-Memory footprint</span>
          <span className="font-mono text-slate-300">{health.memory_usage_mb} MB</span>
        </div>
      </div>
    </div>
  );
}
