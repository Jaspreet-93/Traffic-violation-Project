import React from 'react';
import { Activity, ShieldCheck } from 'lucide-react';

export default function CameraTable({ items, onSelect }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-950/60 text-[10px] text-slate-500 uppercase tracking-wider font-bold border-b border-slate-850">
            <th className="p-4">Name</th>
            <th className="p-4">Resolution</th>
            <th className="p-4">FPS</th>
            <th className="p-4">Status</th>
            <th className="p-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-850 text-xs font-semibold">
          {items.map((item) => (
            <tr key={item.id} className="hover:bg-slate-950/20 text-slate-350">
              <td className="p-4 font-bold text-slate-200">{item.name}</td>
              <td className="p-4 font-mono text-slate-400">{item.resolution}</td>
              <td className="p-4 font-mono text-slate-400">{item.fps}</td>
              <td className="p-4">
                <span className={`px-2 py-0.5 rounded text-[8px] font-bold uppercase ${
                  item.status === 'Online' ? 'bg-emerald-500/10 text-emerald-450 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-450 border border-rose-500/20'
                }`}>
                  {item.status}
                </span>
              </td>
              <td className="p-4 text-right">
                <button
                  onClick={() => onSelect(item.id)}
                  className="px-2.5 py-1 bg-slate-950 border border-slate-850 rounded hover:border-purple-500 hover:text-purple-400 text-slate-400 text-[10px] flex items-center space-x-1 ml-auto cursor-pointer font-bold"
                >
                  <Activity className="w-3 h-3" />
                  <span>Inspect</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
