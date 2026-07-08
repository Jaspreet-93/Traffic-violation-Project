import React from 'react';
import { Database, FileText, CheckCircle } from 'lucide-react';

export default function AuditTrail({ audit }) {
  if (!audit) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Database className="w-4.5 h-4.5 text-purple-400" />
        <span>Hardware & Model Audit Trail</span>
      </h3>

      <div className="space-y-3.5 text-xs">
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500 font-semibold">Decision Timestamp</span>
          <span className="font-mono text-slate-350">{audit.decision_time}</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500 font-semibold">Evidence Log Ref</span>
          <span className="font-mono text-slate-350">{audit.evidence_reference}</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500 font-semibold">Pipeline Processing Duration</span>
          <span className="font-mono text-slate-350 font-bold">{audit.processing_time_ms} ms</span>
        </div>

        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500 font-semibold">AURA Engine status</span>
          <span className="text-emerald-450 font-bold flex items-center space-x-1">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Active</span>
          </span>
        </div>

        <div>
          <span className="text-[10px] text-slate-550 uppercase font-bold tracking-wider block mb-1">Models Audited</span>
          <div className="space-y-1.5">
            {audit.models_used.map((model, idx) => (
              <div key={idx} className="bg-slate-950/20 p-2 rounded border border-slate-850/50 flex items-center space-x-2 text-slate-400 font-semibold">
                <FileText className="w-3.5 h-3.5 text-purple-400" />
                <span>{model}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
