import React from 'react';
import { ShieldCheck, Download, Trash2, Calendar, FileText } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function EvidenceDetails({ activeId, metadata, integrity, onDelete }) {
  if (!activeId || !metadata) return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-500 text-xs">
      Select an evidence item from the grid to inspect details.
    </div>
  );

  const previewUrl = evidenceAPI.getPreviewUrl(activeId);
  const downloadUrl = evidenceAPI.getDownloadUrl(activeId);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg p-5 space-y-4">
      {/* Title */}
      <div className="flex justify-between items-center text-xs border-b border-slate-850 pb-3">
        <h3 className="font-semibold text-slate-250 uppercase tracking-wider">Inspect Evidence Control</h3>
        <span className="text-[10px] text-purple-400 font-bold bg-slate-950 px-2.5 py-1 rounded border border-slate-850">
          ID: #{activeId}
        </span>
      </div>

      {/* Preview Canvas */}
      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-955 flex items-center justify-center min-h-[220px]">
        <img
          src={previewUrl}
          alt={`preview-${activeId}`}
          className="w-full object-contain max-h-[220px]"
        />
        <div className="absolute top-2 left-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
          <ShieldCheck className="w-3 h-3" />
          <span>Processed Overlay</span>
        </div>
      </div>

      {/* Metadata grid */}
      <div className="space-y-2">
        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Metadata Registry</span>
        <div className="bg-slate-950/40 border border-slate-850 rounded-lg p-3 space-y-2 text-xs font-semibold">
          <div className="flex justify-between">
            <span className="text-slate-500">Violation Category</span>
            <span className="text-slate-250 capitalize">{metadata.violation || 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Vehicle ID</span>
            <span className="text-slate-250 font-mono">#{metadata.vehicle_id}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Plate Number</span>
            <span className="text-slate-250 font-mono">{metadata.plate_number || 'UNKNOWN'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Log Timestamp</span>
            <span className="text-slate-250 font-mono">{metadata.timestamp}</span>
          </div>
        </div>
      </div>

      {/* Integrity Verification Check */}
      {integrity && (
        <div className="space-y-2">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">SHA-256 Integrity status</span>
          <div className="bg-slate-950/40 border border-slate-850 rounded-lg p-3 space-y-2 text-[10px] font-semibold">
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Hash Checksum</span>
              <span className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/25 text-emerald-450 rounded text-[9px] font-bold">
                {integrity.status}
              </span>
            </div>
            <p className="text-slate-500 font-mono break-all bg-slate-955 p-2 rounded border border-slate-850/60 leading-normal">
              {integrity.hash}
            </p>
          </div>
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-2 pt-2">
        <a
          href={downloadUrl}
          download={`evidence_${activeId}.jpg`}
          className="flex-1 bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2 rounded-xl text-xs flex items-center justify-center space-x-1.5 transition-all cursor-pointer text-center"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Download JPG</span>
        </a>
        <button
          onClick={() => onDelete(activeId)}
          className="px-3 py-2 bg-slate-955 border border-slate-850 hover:bg-rose-500/10 text-slate-400 hover:text-rose-500 rounded-xl transition-all cursor-pointer"
          title="Delete log"
        >
          <Trash2 className="w-3.5 h-3.5" />
        </button>
      </div>
    </div>
  );
}
