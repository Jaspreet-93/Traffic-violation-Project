import React from 'react';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

export default function VerificationStatus({ verification }) {
  if (!verification) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-slate-200">Integrity Check Verification Status</h3>
        <span className={`px-2.5 py-0.5 rounded border text-[9px] font-bold uppercase tracking-wider ${
          verification.overall_passed
            ? 'text-emerald-450 bg-emerald-500/5 border-emerald-500/10'
            : 'text-rose-450 bg-rose-500/5 border-rose-500/10'
        }`}>
          {verification.overall_passed ? 'System Verified' : 'Action Required'}
        </span>
      </div>

      <div className="space-y-3">
        {verification.checks.map((c, idx) => (
          <div key={idx} className="bg-slate-955 border border-slate-850 p-3 rounded-lg flex items-start space-x-3 text-xs">
            {c.passed ? (
              <ShieldCheck className="w-4.5 h-4.5 text-emerald-450 flex-shrink-0 mt-0.5" />
            ) : (
              <ShieldAlert className="w-4.5 h-4.5 text-rose-450 flex-shrink-0 mt-0.5" />
            )}
            <div className="space-y-0.5 font-semibold">
              <div className="text-slate-200">{c.check_name}</div>
              <div className="text-[10px] text-slate-500 leading-normal">{c.details}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
