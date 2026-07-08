import React from 'react';
import { History, ShieldCheck } from 'lucide-react';

export default function ConfidenceHistory({ historyList }) {
  if (!historyList || historyList.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <History className="w-4 h-4 text-purple-400" />
          <span>Inference Confidence logs</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Job ID</th>
              <th className="p-4">Timestamp</th>
              <th className="p-4">Model Description</th>
              <th className="p-4 w-28">Confidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {historyList.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors text-slate-300">
                <td className="p-4 font-mono font-bold text-slate-200">{item.job_id}</td>
                <td className="p-4 text-slate-400 font-mono text-[10px]">{item.timestamp}</td>
                <td className="p-4 text-slate-450">{item.model_name}</td>
                <td className="p-4 font-bold text-emerald-405 font-mono">
                  {(item.confidence_score * 100).toFixed(0)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
