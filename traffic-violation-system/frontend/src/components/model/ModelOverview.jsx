import React from 'react';
import { Cpu, Video } from 'lucide-react';

export default function ModelOverview({ overview }) {
  if (!overview) return null;

  const items = [
    { label: 'Model Name', value: overview.model_name },
    { label: 'Active Status', value: overview.status, highlight: true },
    { label: 'Inference Speed', value: `${overview.inference_time_ms} ms`, isMono: true },
    { label: 'Average Confidence', value: `${overview.avg_confidence_pct}%`, isMono: true }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Cpu className="w-4.5 h-4.5 text-purple-400" />
        <span>Inference Model Specifications</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-semibold">
        {items.map((item, idx) => (
          <div key={idx} className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
            <span className="text-slate-500">{item.label}</span>
            <span className={`${
              item.highlight ? 'text-emerald-450' : item.isMono ? 'font-mono text-slate-350' : 'text-slate-250'
            }`}>
              {item.value}
            </span>
          </div>
        ))}
      </div>

      <div className="border-t border-slate-850 pt-4 space-y-2">
        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Loaded Sub-Models</span>
        <div className="flex flex-wrap gap-2">
          {overview.loaded_models.map((m, idx) => (
            <span key={idx} className="px-2.5 py-1 bg-slate-955 border border-slate-850 text-slate-350 rounded text-[10px] font-bold">
              {m}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
