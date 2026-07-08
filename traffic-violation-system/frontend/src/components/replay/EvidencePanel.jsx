import React from 'react';
import { Image, Download } from 'lucide-react';

export default function EvidencePanel({ violationId }) {
  const cropUrl = `/uploads/evidence_${violationId}_crop.jpg`;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Image className="w-4.5 h-4.5 text-purple-400" />
        <span>Evidence Crop Summary</span>
      </h3>

      <div className="space-y-4">
        {/* Render crop image box */}
        <div className="rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center min-h-[140px]">
          <span className="text-[10px] text-slate-550 italic">Crop file reference matching violation</span>
        </div>

        {/* Download action */}
        <button
          type="button"
          className="w-full py-2 bg-slate-950 hover:bg-slate-950/80 border border-slate-800 text-slate-350 font-semibold rounded-lg text-xs flex items-center justify-center space-x-1.5 transition-all cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Save Evidence Crop</span>
        </button>
      </div>
    </div>
  );
}
