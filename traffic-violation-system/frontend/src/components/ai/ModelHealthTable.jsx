import React from 'react';
import { Cpu, CheckCircle, XCircle } from 'lucide-react';

export default function ModelHealthTable({ models }) {
  if (!models || models.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span>Active Classifier Models Directory</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Model Details</th>
              <th className="p-4">Status</th>
              <th className="p-4">Weight File</th>
              <th className="p-4">Framework</th>
              <th className="p-4">Input Size</th>
              <th className="p-4">Inference Latency</th>
              <th className="p-4">Throughput</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {models.map((m, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors text-slate-300">
                <td className="p-4">
                  <span className="font-bold text-slate-100 block">{m.name}</span>
                  <span className="text-[10px] text-slate-500 font-mono">v{m.version}</span>
                </td>
                <td className="p-4">
                  {m.status === 'Running' ? (
                    <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-0.5 rounded text-emerald-450 text-[10px] font-bold uppercase w-fit">
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Running</span>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-1.5 bg-rose-500/10 border border-rose-500/20 px-2.5 py-0.5 rounded text-rose-450 text-[10px] font-bold uppercase w-fit">
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Error</span>
                    </div>
                  )}
                </td>
                <td className="p-4 text-slate-400 font-mono text-[10px]">{m.weight_file}</td>
                <td className="p-4 text-slate-400">{m.framework}</td>
                <td className="p-4 text-slate-400 font-mono">{m.input_size}</td>
                <td className="p-4 font-bold text-indigo-400 font-mono">{m.inference_time} ms</td>
                <td className="p-4 font-bold text-purple-400 font-mono">{m.fps} FPS</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
