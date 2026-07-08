import React from 'react';
import { Maximize } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function PreviewPanel({ evidenceId }) {
  if (!evidenceId) return null;

  const previewUrl = evidenceAPI.getPreviewUrl(evidenceId);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider">Quick Preview</h4>
      <div className="rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center min-h-[140px]">
        <img
          src={previewUrl}
          alt={`quick-preview-${evidenceId}`}
          className="w-full object-contain max-h-[140px]"
        />
      </div>
    </div>
  );
}
