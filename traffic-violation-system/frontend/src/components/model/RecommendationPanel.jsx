import React from 'react';
import { Lightbulb } from 'lucide-react';

export default function RecommendationPanel({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Lightbulb className="w-4.5 h-4.5 text-purple-400" />
        <span>Optimizations Recommendations</span>
      </h3>

      <div className="space-y-3.5 max-h-[300px] overflow-y-auto pr-1">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="flex items-start space-x-3 text-xs p-3 bg-purple-500/5 border border-purple-500/10 rounded-lg text-slate-300 leading-relaxed font-semibold">
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 mt-1 flex-shrink-0"></span>
            <span>{rec}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
