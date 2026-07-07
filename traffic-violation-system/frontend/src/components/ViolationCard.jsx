import React from 'react';
import { ShieldAlert, Calendar, Star, Eye } from 'lucide-react';

export default function ViolationCard({ item, onViewEvidence }) {
  const getBadgeStyle = (type) => {
    const term = type.toLowerCase();
    if (term.includes('red light')) return 'bg-rose-500/10 text-rose-450 border-rose-500/20';
    if (term.includes('helmet')) return 'bg-amber-500/10 text-amber-450 border-amber-500/20';
    if (term.includes('seatbelt')) return 'bg-sky-500/10 text-sky-450 border-sky-500/20';
    return 'bg-purple-500/10 text-purple-450 border-purple-500/20';
  };

  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-xl p-4 transition-all hover:shadow-xl hover:-translate-y-0.5 group">
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">
            <ShieldAlert className="w-5 h-5 text-rose-500" />
          </div>
          <div>
            <h4 className="font-bold text-slate-100 group-hover:text-purple-400 transition-colors">
              Vehicle #{item.vehicle_id}
            </h4>
            <span className="text-xs text-slate-500">License: {item.plate_number || 'PB10AB1234'}</span>
          </div>
        </div>
        <span className={`text-[10px] uppercase font-bold tracking-wider px-2.5 py-1 rounded-full border ${getBadgeStyle(item.violation)}`}>
          {item.violation}
        </span>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-850 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center space-x-1.5">
          <Star className="w-3.5 h-3.5 text-amber-500" />
          <span>Confidence: {(item.confidence * 100).toFixed(0)}%</span>
        </div>
        {onViewEvidence && (
          <button
            onClick={onViewEvidence}
            className="flex items-center space-x-1 text-purple-400 hover:text-purple-300 font-semibold transition-colors"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Proof</span>
          </button>
        )}
      </div>
    </div>
  );
}
