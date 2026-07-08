import React from 'react';
import { Database, ShieldCheck, ShieldAlert } from 'lucide-react';

export default function DatasetHealth({ datasets }) {
  if (!datasets || datasets.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Database className="w-4 h-4 text-purple-400" />
          <span>Active Datasets Health Directory</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Dataset Name</th>
              <th className="p-4">Purpose</th>
              <th className="p-4 w-28">Health Score</th>
              <th className="p-4">Train Split</th>
              <th className="p-4">Val Split</th>
              <th className="p-4">Test Split</th>
              <th className="p-4">Format</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {datasets.map((d, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors text-slate-300">
                <td className="p-4">
                  <span className="font-bold text-slate-100 block">{d.dataset_name}</span>
                  <span className="text-[10px] text-slate-500 font-mono">Classes: {d.classes.join(', ')}</span>
                </td>
                <td className="p-4 text-slate-400">{d.purpose}</td>
                <td className="p-4">
                  {d.dataset_health_score > 0 ? (
                    <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded text-emerald-450 text-[10px] font-bold uppercase w-fit">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>{d.dataset_health_score.toFixed(0)}%</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 bg-rose-500/10 border border-rose-500/20 px-2.5 py-0.5 rounded text-rose-450 text-[10px] font-bold uppercase w-fit">
                      <ShieldAlert className="w-3.5 h-3.5" />
                      <span>Missing</span>
                    </div>
                  )}
                </td>
                <td className="p-4 text-slate-400 font-mono">{d.training_images}</td>
                <td className="p-4 text-slate-400 font-mono">{d.validation_images}</td>
                <td className="p-4 text-slate-400 font-mono">{d.test_images}</td>
                <td className="p-4 text-slate-500 font-mono text-[10px]">{d.annotation_format}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
