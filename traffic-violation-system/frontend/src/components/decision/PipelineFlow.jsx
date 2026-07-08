import React from 'react';
import { Play, ArrowRight, ShieldCheck, Mail, Database } from 'lucide-react';

export default function PipelineFlow() {
  const steps = [
    "Raw Feed",
    "YOLO Detector",
    "Tracking",
    "Classifiers",
    "Rule Engine",
    "Database Stored"
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Play className="w-4.5 h-4.5 text-purple-400" />
        <span>Horizontal Pipeline Schema Flow</span>
      </h3>

      <div className="flex flex-wrap items-center justify-between gap-3 text-xs font-semibold">
        {steps.map((step, idx) => (
          <React.Fragment key={idx}>
            <div className="bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg flex items-center space-x-2 text-slate-350">
              <span className="w-4 h-4 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 flex items-center justify-center font-bold font-mono text-[10px]">
                {idx + 1}
              </span>
              <span>{step}</span>
            </div>
            {idx < steps.length - 1 && <ArrowRight className="w-4 h-4 text-slate-650 flex-shrink-0" />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}
