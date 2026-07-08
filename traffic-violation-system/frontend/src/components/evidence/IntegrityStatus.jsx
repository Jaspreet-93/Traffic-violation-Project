import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function IntegrityStatus({ integrity }) {
  if (!integrity) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <ShieldCheck className="w-4.5 h-4.5 text-purple-400" />
        <span>File Integrity Verification</span>
      </h3>

      <div className="space-y-3.5 text-xs font-semibold">
        {/* SHA-256 Checksum */}
        <div className="space-y-1">
          <span className="text-slate-500 uppercase text-[9px] tracking-wider block">SHA-256 Checksum</span>
          <div className="bg-slate-950 p-2.5 rounded border border-slate-850 text-slate-400 font-mono break-all leading-relaxed text-[10px]">
            {integrity.checksum_sha256}
          </div>
        </div>

        {/* Status */}
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Secure Audit Check</span>
          <span className="text-emerald-450 uppercase font-mono font-bold">{integrity.status}</span>
        </div>
      </div>
    </div>
  );
}
