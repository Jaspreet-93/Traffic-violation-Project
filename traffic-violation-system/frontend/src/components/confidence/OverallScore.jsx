import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';

export default function OverallScore({ trust }) {
  if (!trust) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <div className="flex items-center justify-between text-xs font-semibold text-slate-200">
        <span className="flex items-center space-x-2">
          <ShieldCheck className="w-4.5 h-4.5 text-purple-400" />
          <span>Trust Rating Quality Score</span>
        </span>
        <span className="text-purple-400 font-bold font-mono">{trust.overall_trust_score}%</span>
      </div>

      <div className="w-full bg-slate-950 rounded-full h-2.5 overflow-hidden border border-slate-850">
        <div
          className="bg-purple-650 h-2.5 rounded-full transition-all duration-300"
          style={{ width: `${trust.overall_trust_score}%` }}
        ></div>
      </div>

      <div className="bg-slate-955 p-3 rounded-lg border border-slate-850 flex items-start space-x-2 text-[10px] text-slate-500 leading-relaxed font-semibold">
        <Info className="w-3.5 h-3.5 mt-0.5 text-purple-400 flex-shrink-0" />
        <span>Overall system integrity is marked as Excellent based on active models alignment configurations.</span>
      </div>
    </div>
  );
}
