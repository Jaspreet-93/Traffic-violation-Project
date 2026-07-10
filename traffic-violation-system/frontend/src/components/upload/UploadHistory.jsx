import React from 'react';
import { History, Eye, Trash2, FileImage, FileVideo, CheckCircle2, Loader2, XCircle } from 'lucide-react';

export default function UploadHistory({ historyList, onView, onDelete }) {
  if (!historyList || historyList.length === 0) {
    return (
      <div className="relative bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-8 text-center shadow-2xl space-y-3 overflow-hidden">
        <div className="absolute -top-12 -left-12 w-24 h-24 bg-purple-650/5 rounded-full blur-2xl pointer-events-none"></div>
        <History className="w-10 h-10 text-slate-700 mx-auto mb-1 animate-pulse" />
        <h4 className="text-sm font-bold text-slate-350 tracking-wide uppercase">No Upload Logs Present</h4>
        <p className="text-[11px] text-slate-500 max-w-sm mx-auto leading-relaxed">
          Begin by dragging and dropping surveillance footage or camera snapshots in the console above.
        </p>
      </div>
    );
  }

  return (
    <div className="relative bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl overflow-hidden shadow-2xl">
      {/* Table Header Wrapper */}
      <div className="bg-slate-950/80 px-6 py-4 border-b border-slate-800/80 flex items-center justify-between">
        <div className="space-y-1">
          <h3 className="font-bold text-sm text-slate-100 flex items-center space-x-2.5">
            <History className="w-4 h-4 text-purple-400" />
            <span className="tracking-wide uppercase text-xs">Surveillance Upload Logs</span>
          </h3>
          <p className="text-[10px] text-slate-400">Audit index of previous media pipeline executions and results.</p>
        </div>
        <div className="bg-slate-900 border border-slate-850 px-2.5 py-1 rounded-full text-[10px] text-slate-400 font-mono">
          Total Logs: <span className="text-purple-400 font-bold">{historyList.length}</span>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/30 border-b border-slate-850 text-slate-450 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4 pl-6">Filename</th>
              <th className="p-4">Upload Date</th>
              <th className="p-4">Type</th>
              <th className="p-4">Status</th>
              <th className="p-4">Summary</th>
              <th className="p-4 text-center w-28 pr-6">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850/60">
            {historyList.map((item, idx) => (
              <tr 
                key={idx} 
                className="group hover:bg-slate-850/20 transition-all duration-200 text-slate-350"
              >
                <td className="p-4 pl-6 font-semibold text-slate-200 group-hover:text-purple-300 transition-colors max-w-[200px] truncate">
                  {item.filename}
                </td>
                <td className="p-4 text-slate-400 font-mono text-[10px]">{item.upload_date}</td>
                <td className="p-4">
                  {item.file_type === 'video' ? (
                    <span className="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded-md text-[10px] font-medium bg-purple-500/10 border border-purple-500/20 text-purple-300">
                      <FileVideo className="w-3 h-3 text-purple-400 shrink-0" />
                      <span>Video</span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center space-x-1.5 px-2 py-0.5 rounded-md text-[10px] font-medium bg-sky-500/10 border border-sky-500/20 text-sky-300">
                      <FileImage className="w-3 h-3 text-sky-400 shrink-0" />
                      <span>Image</span>
                    </span>
                  )}
                </td>
                <td className="p-4 font-mono">
                  {item.status === 'Completed' ? (
                    <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                      <CheckCircle2 className="w-2.5 h-2.5 text-emerald-400 shrink-0" />
                      <span>Completed</span>
                    </span>
                  ) : item.status === 'Processing' ? (
                    <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-indigo-500/10 border border-indigo-500/20 text-indigo-400">
                      <Loader2 className="w-2.5 h-2.5 text-indigo-400 animate-spin shrink-0" />
                      <span>Processing</span>
                    </span>
                  ) : (
                    <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md text-[10px] font-bold bg-rose-500/10 border border-rose-500/20 text-rose-400">
                      <XCircle className="w-2.5 h-2.5 text-rose-400 shrink-0" />
                      <span>Failed</span>
                    </span>
                  )}
                </td>
                <td className="p-4 text-slate-400 leading-relaxed text-[11px] max-w-[280px] truncate" title={item.summary_text}>
                  {item.summary_text}
                </td>
                <td className="p-4 pr-6">
                  <div className="flex items-center justify-center space-x-3">
                    {item.status === 'Completed' && (
                      <button
                        onClick={() => onView(item.job_id)}
                        className="p-1.5 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-purple-500/30 hover:bg-purple-500/10 text-slate-400 hover:text-purple-300 transition-all duration-200 cursor-pointer shadow-md group-hover:scale-105"
                        title="Visualize result canvas"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </button>
                    )}
                    <button
                      onClick={() => onDelete(item.job_id)}
                      className="p-1.5 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-rose-500/30 hover:bg-rose-500/10 text-slate-400 hover:text-rose-450 transition-all duration-200 cursor-pointer shadow-md group-hover:scale-105"
                      title="Purge log from database"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
