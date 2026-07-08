import React from 'react';
import { History, Eye, Trash2, FileImage, FileVideo, ShieldCheck, ShieldAlert } from 'lucide-react';

export default function UploadHistory({ historyList, onView, onDelete }) {
  if (!historyList || historyList.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center shadow-md">
        <History className="w-8 h-8 text-slate-700 mx-auto mb-2" />
        <h4 className="text-xs font-semibold text-slate-400">No Upload History Found</h4>
        <p className="text-[10px] text-slate-600 mt-1">Upload images or videos above to verify detections pipeline.</p>
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <History className="w-4 h-4 text-purple-400" />
          <span>Surveillance Upload Logs</span>
        </h3>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950/40 border-b border-slate-850 text-slate-400 font-bold uppercase text-[9px] tracking-wider">
              <th className="p-4">Filename</th>
              <th className="p-4">Upload Date</th>
              <th className="p-4">Type</th>
              <th className="p-4">Status</th>
              <th className="p-4">Summary</th>
              <th className="p-4 text-center w-28">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {historyList.map((item, idx) => (
              <tr key={idx} className="hover:bg-slate-955 transition-colors text-slate-350">
                <td className="p-4 font-bold text-slate-200">{item.filename}</td>
                <td className="p-4 text-slate-400 font-mono text-[10px]">{item.upload_date}</td>
                <td className="p-4">
                  {item.file_type === 'video' ? (
                    <span className="flex items-center space-x-1">
                      <FileVideo className="w-3.5 h-3.5 text-purple-400" />
                      <span>Video</span>
                    </span>
                  ) : (
                    <span className="flex items-center space-x-1">
                      <FileImage className="w-3.5 h-3.5 text-sky-400" />
                      <span>Image</span>
                    </span>
                  )}
                </td>
                <td className="p-4 font-mono">
                  {item.status === 'Completed' ? (
                    <span className="text-emerald-500 font-semibold">{item.status}</span>
                  ) : item.status === 'Processing' ? (
                    <span className="text-indigo-400 font-semibold animate-pulse">{item.status}...</span>
                  ) : (
                    <span className="text-rose-500 font-semibold">{item.status}</span>
                  )}
                </td>
                <td className="p-4 text-slate-450 leading-relaxed text-[11px] truncate max-w-[240px]">
                  {item.summary_text}
                </td>
                <td className="p-4">
                  <div className="flex items-center justify-center space-x-2.5">
                    {item.status === 'Completed' && (
                      <button
                        onClick={() => onView(item.job_id)}
                        className="p-1.5 rounded bg-slate-950 hover:bg-purple-500/10 text-slate-350 hover:text-purple-400 transition-all cursor-pointer"
                        title="View result canvas"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    )}
                    <button
                      onClick={() => onDelete(item.job_id)}
                      className="p-1.5 rounded bg-slate-950 hover:bg-rose-500/10 text-slate-350 hover:text-rose-500 transition-all cursor-pointer"
                      title="Purge log"
                    >
                      <Trash2 className="w-4 h-4" />
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
