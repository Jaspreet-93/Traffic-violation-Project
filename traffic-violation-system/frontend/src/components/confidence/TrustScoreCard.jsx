import React from 'react';
import { ShieldAlert, ShieldCheck } from 'lucide-react';

export default function TrustScoreCard({ trust }) {
  if (!trust) return null;

  const getLevelBadge = (level) => {
    if (level === 'Excellent') return 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450';
    if (level === 'Good') return 'bg-sky-500/10 border-sky-500/20 text-sky-400';
    if (level === 'Average') return 'bg-amber-500/10 border-amber-500/20 text-amber-450';
    return 'bg-rose-500/10 border-rose-500/20 text-rose-450';
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <ShieldCheck className="w-4.5 h-4.5 text-purple-400" />
        <span>Overall AI Trust score</span>
      </h3>

      <div className="flex flex-col items-center justify-center space-y-3.5 my-3 flex-1">
        <div className="relative flex items-center justify-center w-28 h-28 rounded-full border-4 border-slate-950 bg-slate-950 shadow-inner">
          <div className="text-center">
            <span className="text-3xl font-extrabold text-slate-100 font-mono tracking-tight">
              {trust.overall_trust_score}%
            </span>
            <span className="text-[9px] text-slate-500 uppercase tracking-widest block font-bold mt-1">Trust Score</span>
          </div>
        </div>

        <span className={`text-xs font-bold px-3 py-1 rounded-full border uppercase ${getLevelBadge(trust.trust_level)}`}>
          Level: {trust.trust_level}
        </span>
      </div>

      <p className="text-[10px] text-slate-500 leading-relaxed text-center font-medium">
        Calculated dynamically from live active camera model inference performance, classification consistency, and frame resolution weights.
      </p>
    </div>
  );
}
// Import Shield from lucide
import { Shield } from 'lucide-react';
