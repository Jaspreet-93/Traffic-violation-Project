import React from 'react';
import { Activity } from 'lucide-react';

export default function CameraHealth({ health }) {
  if (!health) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="font-semibold text-xs text-slate-200 flex items-center space-x-2">
        <Activity className="w-4 h-4 text-purple-400" />
        <span>Hardware Diagnostics Monitor</span>
      </h3>

      <div className="space-y-3 text-xs font-semibold">
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Latency Duration</span>
          <span className="font-mono text-slate-300">{health.latency_ms} ms</span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Packet Loss Rate</span>
          <span className="font-mono text-slate-300">{health.packet_loss_pct}%</span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Video Signal Status</span>
          <span className="text-emerald-450 uppercase font-mono">{health.status}</span>
        </div>
      </div>
    </div>
  );
}
