import React from 'react';
import { ShieldCheck, Clock, ShieldAlert, FileText } from 'lucide-react';

export default function DetectionSummary({ evidence }) {
  if (!evidence) return null;

  const items = [
    { label: "Vehicles Detected", value: evidence.vehicles_count, icon: ShieldCheck, color: "text-purple-400" },
    { label: "Violations Flagged", value: evidence.violations_count, icon: ShieldAlert, color: evidence.violations_count > 0 ? "text-rose-400" : "text-slate-450" },
    { label: "Processing Duration", value: `${evidence.processing_time_sec}s`, icon: Clock, color: "text-sky-400" },
    { label: "Frames Count", value: evidence.frame_count || 1, icon: FileText, color: "text-indigo-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider">Detection Summary Metrics</h4>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        {items.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div key={idx} className="bg-slate-950 border border-slate-850 p-3 rounded-lg flex items-center space-x-3.5">
              <div className={`p-2 rounded-lg bg-slate-900 ${item.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <div>
                <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">{item.label}</span>
                <span className="text-sm font-bold text-slate-200 mt-0.5 block">{item.value}</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-slate-955 p-3 rounded-lg border border-slate-850 text-xs text-slate-400 leading-relaxed font-semibold">
        {evidence.summary_text}
      </div>
    </div>
  );
}
