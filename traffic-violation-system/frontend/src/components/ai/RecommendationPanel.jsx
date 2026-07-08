import React from 'react';
import { HelpCircle, StarCheck, CheckCircle } from 'lucide-react';

export default function RecommendationPanel({ recommendations }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-full justify-between">
      <div>
        <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
          <CheckCircle className="w-4.5 h-4.5 text-purple-400" />
          <span>System Optimization Recommendations</span>
        </h3>

        <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
          {(!recommendations || recommendations.length === 0) ? (
            <div className="text-slate-500 text-xs py-8 text-center">
              No recommendations available. All systems fully optimized.
            </div>
          ) : (
            recommendations.map((rec, idx) => (
              <div key={idx} className="bg-slate-950/60 border border-slate-850 p-3 rounded-lg flex items-start space-x-2 text-xs">
                <span className="bg-purple-650/15 p-1 rounded text-purple-400 mt-0.5 font-bold">
                  {idx + 1}
                </span>
                <span className="text-slate-350 leading-relaxed">{rec}</span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
