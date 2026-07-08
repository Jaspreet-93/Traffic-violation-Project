import React from 'react';
import { Info, Shield } from 'lucide-react';

export default function ReplayInformation({ info }) {
  if (!info) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Info className="w-4.5 h-4.5 text-purple-400" />
        <span>Footage Classification Summary</span>
      </h3>

      <div className="space-y-3 text-xs font-semibold">
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Violation Type</span>
          <span className="text-rose-450 font-bold">{info.violation_type}</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Video Timestamp</span>
          <span className="font-mono text-slate-350">{info.timestamp}</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Pipeline Latency</span>
          <span className="font-mono text-slate-350">{info.processing_time_sec}s</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500 flex items-center space-x-1"><Shield className="w-3.5 h-3.5" /> <span>Trust score</span></span>
          <span className="text-purple-400 font-mono font-bold">{info.overall_trust_score}%</span>
        </div>
      </div>
    </div>
  );
}
