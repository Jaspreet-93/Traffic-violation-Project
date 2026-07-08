import React from 'react';
import { Target, Activity } from 'lucide-react';

export default function ConfidenceReasoning({ confidence, trustScore }) {
  if (!confidence) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Target className="w-4.5 h-4.5 text-purple-400" />
        <span>Statistical Precision Weights</span>
      </h3>

      <div className="space-y-4 text-xs font-semibold">
        {Object.entries(confidence).map(([model, val]) => {
          const num = parseFloat(val.replace('%', '')) || 90;
          return (
            <div key={model} className="space-y-1.5">
              <div className="flex justify-between text-slate-400">
                <span>{model}</span>
                <span className="text-purple-400 font-mono font-bold">{val}</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden border border-slate-850">
                <div
                  className="bg-purple-650 h-1.5 rounded-full transition-all duration-300"
                  style={{ width: `${num}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
