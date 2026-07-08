import React from 'react';
import { Maximize, ShieldCheck } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function EvidenceViewer({ evidenceId }) {
  if (!evidenceId) return null;
  
  const previewUrl = evidenceAPI.getPreviewUrl(evidenceId);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg p-5 space-y-4">
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-slate-200">Footage Preview Inspect Canvas</h3>
        <span className="text-[10px] text-purple-400 font-bold bg-slate-950 px-2.5 py-1 rounded border border-slate-850">
          Evidence: {evidenceId}
        </span>
      </div>

      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center min-h-[300px]">
        <img
          src={previewUrl}
          alt={`preview-${evidenceId}`}
          className="w-full object-contain max-h-[360px]"
        />
        <div className="absolute top-3 left-3 bg-rose-500/10 border border-rose-500/20 text-rose-450 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
          <ShieldCheck className="w-3 h-3 animate-pulse" />
          <span>Processed Overlay Active</span>
        </div>
      </div>
    </div>
  );
}
