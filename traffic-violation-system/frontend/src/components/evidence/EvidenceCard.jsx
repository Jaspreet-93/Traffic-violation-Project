import React from 'react';
import { Calendar, Eye, ShieldCheck, Trash2 } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function EvidenceCard({ item, onSelect, onDelete }) {
  const previewUrl = evidenceAPI.getPreviewUrl(item.evidence_id);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow hover:border-slate-700/80 transition-all flex flex-col group">
      {/* Thumbnail */}
      <div className="relative h-40 bg-slate-950 overflow-hidden flex items-center justify-center border-b border-slate-850">
        <img
          src={previewUrl}
          alt={`evidence-${item.evidence_id}`}
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
        />
        <div className="absolute top-3 left-3 bg-purple-500/10 border border-purple-500/20 text-purple-400 text-[9px] font-bold px-2 py-0.5 rounded">
          ID: {item.evidence_id}
        </div>
      </div>

      {/* Info */}
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        <div className="space-y-1">
          <div className="flex justify-between items-center">
            <h4 className="text-xs font-bold text-slate-200 capitalize">{item.violation}</h4>
            <span className="text-[10px] text-slate-500 font-mono">Veh: {item.vehicle_id}</span>
          </div>
          <div className="text-[10px] text-slate-500 flex items-center space-x-1.5 font-mono">
            <Calendar className="w-3.5 h-3.5" />
            <span>{item.timestamp}</span>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => onSelect(item.evidence_id)}
            className="flex-1 bg-purple-650 hover:bg-purple-750 text-white font-semibold py-1.5 rounded text-[10px] flex items-center justify-center space-x-1 transition-all cursor-pointer"
          >
            <Eye className="w-3 h-3" />
            <span>Inspect</span>
          </button>
          <button
            onClick={() => onDelete(item.evidence_id)}
            className="p-1.5 rounded bg-slate-950 hover:bg-rose-500/10 text-slate-400 hover:text-rose-500 transition-all cursor-pointer border border-slate-850"
            title="Delete log"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
