import React from 'react';
import { Download } from 'lucide-react';

export default function ExportButtons({ onExport }) {
  const formats = [
    { label: 'Export PDF', format: 'pdf', color: 'border-rose-500/20 text-rose-450 hover:bg-rose-500/5' },
    { label: 'Export Excel', format: 'excel', color: 'border-emerald-500/20 text-emerald-450 hover:bg-emerald-500/5' },
    { label: 'Export CSV', format: 'csv', color: 'border-purple-500/20 text-purple-450 hover:bg-purple-500/5' }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider">Quick Export</h4>
      <div className="grid grid-cols-3 gap-3">
        {formats.map((f, idx) => (
          <button
            key={idx}
            onClick={() => onExport(f.format)}
            className={`py-2 px-1 border rounded-lg text-[10px] font-bold uppercase flex flex-col items-center justify-center space-y-1 transition-all cursor-pointer bg-slate-950 ${f.color}`}
          >
            <Download className="w-3.5 h-3.5" />
            <span>{f.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
