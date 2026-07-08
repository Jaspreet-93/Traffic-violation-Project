import React from 'react';
import { ShieldAlert, AlertTriangle, ShieldCheck, Zap } from 'lucide-react';

export default function DiagnosticsPanel({ diagnostics }) {
  const getSeverityBadge = (sev) => {
    if (sev === 'Critical') return 'bg-rose-500/10 border-rose-500/20 text-rose-450';
    if (sev === 'Warning') return 'bg-amber-500/10 border-amber-500/20 text-amber-450';
    return 'bg-purple-500/10 border-purple-500/20 text-purple-450';
  };

  const getSeverityIcon = (sev) => {
    if (sev === 'Critical') return <ShieldAlert className="w-4 h-4 text-rose-500" />;
    return <AlertTriangle className="w-4 h-4 text-amber-500" />;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-full justify-between">
      <div>
        <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
          <Zap className="w-4.5 h-4.5 text-purple-400" />
          <span>Real-Time AI Diagnostics</span>
        </h3>

        <div className="space-y-3.5 max-h-[300px] overflow-y-auto pr-1">
          {(!diagnostics || diagnostics.length === 0) ? (
            <div className="text-center p-8 bg-slate-950/40 border border-slate-850 rounded-xl">
              <ShieldCheck className="w-10 h-10 text-emerald-500 mx-auto mb-2 animate-bounce" />
              <h4 className="text-xs text-slate-400 font-semibold">All Systems Normal</h4>
              <p className="text-[9px] text-slate-600 mt-1">No AI anomalies detected in this session cycle.</p>
            </div>
          ) : (
            diagnostics.map((d, idx) => (
              <div key={idx} className="bg-slate-955 border border-slate-850 p-3 rounded-lg flex flex-col space-y-2 text-xs hover:border-slate-800/80 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-1.5 font-bold text-slate-200">
                    {getSeverityIcon(d.severity)}
                    <span className="truncate max-w-[200px]">{d.problem}</span>
                  </div>
                  <span className={`text-[9px] font-bold px-2 py-0.5 rounded border uppercase ${getSeverityBadge(d.severity)}`}>
                    {d.severity}
                  </span>
                </div>
                <div className="text-[10px] text-slate-500 bg-slate-950 p-2 rounded border border-slate-850/20 leading-relaxed">
                  <strong>Solution:</strong> {d.recommended_solution}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
// Import Zap from lucide
import { AlertCircle } from 'lucide-react';
