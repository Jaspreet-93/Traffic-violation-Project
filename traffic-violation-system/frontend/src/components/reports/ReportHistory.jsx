import React from 'react';
import { Download, Trash2 } from 'lucide-react';
import { reportsAPI } from '../../services/reportsApi';

export default function ReportHistory({ items, onDelete }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-950/60 text-[10px] text-slate-500 uppercase tracking-wider font-bold border-b border-slate-850">
            <th className="p-4">Report Name</th>
            <th className="p-4">Type</th>
            <th className="p-4">Format</th>
            <th className="p-4">Generated At</th>
            <th className="p-4 text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-850 text-xs font-semibold">
          {items.map((item) => {
            const downloadUrl = reportsAPI.getDownloadUrl(item.id);
            return (
              <tr key={item.id} className="hover:bg-slate-950/20 text-slate-350">
                <td className="p-4 font-bold text-slate-200 truncate max-w-[200px]">{item.name}</td>
                <td className="p-4 capitalize text-slate-400">{item.report_type}</td>
                <td className="p-4 uppercase text-slate-400 font-mono">{item.export_format}</td>
                <td className="p-4 text-slate-500 font-mono">{item.generated_at}</td>
                <td className="p-4 text-right flex items-center justify-end space-x-2">
                  <a
                    href={downloadUrl}
                    download
                    className="p-1.5 rounded bg-slate-950 border border-slate-850 text-slate-400 hover:text-purple-400 transition-all"
                    title="Download File"
                  >
                    <Download className="w-3.5 h-3.5" />
                  </a>
                  <button
                    onClick={() => onDelete(item.id)}
                    className="p-1.5 rounded bg-slate-950 border border-slate-850 text-slate-400 hover:text-rose-500 transition-all cursor-pointer"
                    title="Clear log"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
