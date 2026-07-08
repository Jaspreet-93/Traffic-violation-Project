import React from 'react';
import { Download } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function DownloadPanel({ evidenceId }) {
  if (!evidenceId) return null;

  const downloadUrl = evidenceAPI.getDownloadUrl(evidenceId);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider">Export Panel</h4>
      
      <a
        href={downloadUrl}
        download={`evidence_${evidenceId}.jpg`}
        className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-lg text-xs flex items-center justify-center space-x-1.5 shadow transition-all cursor-pointer"
      >
        <Download className="w-3.5 h-3.5" />
        <span>Download Evidence Package</span>
      </a>
    </div>
  );
}
