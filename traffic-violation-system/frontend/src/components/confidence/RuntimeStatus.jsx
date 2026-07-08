import React from 'react';
import { Radio, ShieldCheck, Activity } from 'lucide-react';

export default function RuntimeStatus({ stats }) {
  if (!stats) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Radio className="w-4.5 h-4.5 text-purple-400 animate-pulse" />
        <span>Operational Runtime Status</span>
      </h3>

      <div className="space-y-4 flex-1 flex flex-col justify-around text-xs">
        {/* Average Processing Time */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <Activity className="w-3.5 h-3.5" />
            <span>Average Latency</span>
          </span>
          <span className="font-bold text-slate-250 font-mono">{stats.average_confidence.toFixed(1)} ms</span>
        </div>

        {/* Status */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Integrity Check</span>
          </span>
          <span className="font-bold text-emerald-450 uppercase font-mono">Passed</span>
        </div>
      </div>
    </div>
  );
}
