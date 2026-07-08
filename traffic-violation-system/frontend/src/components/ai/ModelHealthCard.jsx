import React from 'react';
import { Cpu, CheckCircle, XCircle } from 'lucide-react';

export default function ModelHealthCard({ modelData }) {
  if (!modelData || modelData.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span>Pipeline Classifier Models Health</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Model Description</th>
              <th className="p-4">Status</th>
              <th className="p-4">Exists</th>
              <th className="p-4">Loads Successfully</th>
              <th className="p-4">Device</th>
              <th className="p-4">Framework</th>
              <th className="p-4">Detectable Classes</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {modelData.map((m, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors text-slate-350">
                <td className="p-4 font-bold text-slate-200">{m.name}</td>
                <td className="p-4">
                  {m.status === 'Healthy' ? (
                    <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-450 font-bold uppercase px-2 py-0.5 rounded text-[10px]">Healthy</span>
                  ) : (
                    <span className="bg-rose-500/10 border border-rose-500/20 text-rose-450 font-bold uppercase px-2 py-0.5 rounded text-[10px]">{m.status}</span>
                  )}
                </td>
                <td className="p-4 font-mono">{m.exists ? 'Yes' : 'No'}</td>
                <td className="p-4 font-mono">{m.loads_successfully ? 'Yes' : 'No'}</td>
                <td className="p-4 font-mono text-slate-400">{m.device}</td>
                <td className="p-4 text-slate-400">{m.framework}</td>
                <td className="p-4 text-slate-500 font-mono text-[10px]">{m.classes.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
