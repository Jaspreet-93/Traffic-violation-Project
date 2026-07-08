import React from 'react';
import { Cpu, Calendar, Tag, ShieldCheck } from 'lucide-react';

export default function DecisionCard({ decision }) {
  if (!decision) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <div className="space-y-4">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4.5 h-4.5 text-purple-400" />
          <span>Latest AI Violation Verdict</span>
        </h3>

        <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-lg space-y-3.5">
          <div className="flex justify-between text-xs text-slate-450">
            <span className="flex items-center space-x-1.5"><Tag className="w-3.5 h-3.5" /> <span>Violation ID</span></span>
            <span className="font-mono font-bold text-slate-350">{decision.violation_id}</span>
          </div>

          <div className="flex justify-between text-xs text-slate-450">
            <span className="flex items-center space-x-1.5"><Calendar className="w-3.5 h-3.5" /> <span>Decision Time</span></span>
            <span className="font-mono text-slate-350">{decision.timestamp}</span>
          </div>

          <div className="flex justify-between text-xs text-slate-450">
            <span className="flex items-center space-x-1.5"><ShieldCheck className="w-3.5 h-3.5" /> <span>Classification</span></span>
            <span className="font-bold text-rose-450">{decision.violation_type}</span>
          </div>
        </div>

        <div className="bg-slate-955 p-3 rounded-lg border border-slate-850 text-xs text-slate-400 leading-relaxed font-semibold">
          {decision.decision}
        </div>
      </div>
    </div>
  );
}
