import React from 'react';
import { History, Eye } from 'lucide-react';

export default function DecisionSummary({ historyList, onSelect }) {
  if (!historyList || historyList.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <History className="w-4 h-4 text-purple-400" />
          <span>Surveillance Decision History log</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Violation ID</th>
              <th className="p-4">Timestamp</th>
              <th className="p-4">Infraction Class</th>
              <th className="p-4">Status</th>
              <th className="p-4 w-28 text-center">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850 text-slate-350">
            {historyList.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors">
                <td className="p-4 font-mono font-bold text-slate-250">{item.violation_id}</td>
                <td className="p-4 text-slate-400 font-mono text-[10px]">{item.timestamp}</td>
                <td className="p-4 font-semibold">{item.violation_type}</td>
                <td className="p-4 font-bold">
                  {item.status === 'Approved' ? (
                    <span className="text-emerald-500">{item.status}</span>
                  ) : (
                    <span className="text-rose-500 animate-pulse">{item.status}</span>
                  )}
                </td>
                <td className="p-4 text-center">
                  <button
                    onClick={() => onSelect(item.violation_id)}
                    className="p-1.5 rounded bg-slate-950 hover:bg-purple-500/10 text-slate-350 hover:text-purple-400 transition-all cursor-pointer"
                    title="Audit trail logs"
                  >
                    <Eye className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
