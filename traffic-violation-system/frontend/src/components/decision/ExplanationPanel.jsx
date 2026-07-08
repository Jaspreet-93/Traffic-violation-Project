import React from 'react';
import { Eye, ShieldAlert, Cpu } from 'lucide-react';

export default function ExplanationPanel({ explanation }) {
  if (!explanation) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <ShieldAlert className="w-4.5 h-4.5 text-purple-400" />
        <span>Explainable AI Reasoning Log</span>
      </h3>

      <div className="space-y-3 text-xs leading-relaxed">
        {/* Violation & Final */}
        <div className="flex justify-between items-center border-b border-slate-850 pb-2 font-semibold">
          <span className="text-slate-450 uppercase text-[9px] tracking-wider">Classification</span>
          <span className="text-slate-200 font-bold">{explanation.violation_type}</span>
        </div>

        {/* Reason Text */}
        <div className="bg-slate-950/40 p-3 rounded border border-slate-850 text-slate-400 font-medium">
          {explanation.reason}
        </div>

        {/* Supporting Checks */}
        <div>
          <span className="text-[10px] text-slate-550 uppercase font-bold tracking-wider block mb-1">Supporting Detections</span>
          <div className="flex flex-wrap gap-2">
            {explanation.supporting_detections.map((s, idx) => (
              <span key={idx} className="bg-purple-500/5 border border-purple-500/10 text-purple-400 font-bold px-2 py-0.5 rounded text-[10px]">
                {s}
              </span>
            ))}
          </div>
        </div>

        {/* Confidence ratings */}
        <div>
          <span className="text-[10px] text-slate-555 uppercase font-bold tracking-wider block mb-1">Inference Confidence Level</span>
          <div className="space-y-1.5">
            {Object.entries(explanation.model_confidence).map(([key, val]) => (
              <div key={key} className="flex justify-between text-[11px] text-slate-400 font-semibold bg-slate-950/20 px-2 py-1 rounded border border-slate-850/50">
                <span>{key}</span>
                <span className="text-purple-400 font-mono font-bold">{val}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Decision Output */}
        <div className="flex justify-between items-center border-t border-slate-850 pt-2 font-semibold text-[11px]">
          <span className="text-slate-450 uppercase text-[9px] tracking-wider">Verdict Status</span>
          <span className="text-emerald-450 font-bold">{explanation.final_decision}</span>
        </div>
      </div>
    </div>
  );
}
// Import Shield from lucide
import { Shield } from 'lucide-react';
