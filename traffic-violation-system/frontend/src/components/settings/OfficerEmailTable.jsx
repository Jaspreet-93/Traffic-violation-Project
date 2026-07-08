import React from 'react';
import { Edit2, Trash2, CheckCircle, Star } from 'lucide-react';

export default function OfficerEmailTable({ emails, onEdit, onDelete, onToggleStatus, onSetPrimary }) {
  if (!emails || emails.length === 0) {
    return (
      <div className="p-8 text-center text-xs text-slate-500 font-semibold bg-slate-950/20 border border-slate-850 rounded-xl">
        No officer emails registered. Add one below to start receiving violation alerts.
      </div>
    );
  }

  return (
    <div className="bg-slate-950/20 border border-slate-850 rounded-xl overflow-hidden shadow">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-950/60 text-[10px] text-slate-500 uppercase tracking-wider font-bold border-b border-slate-850">
              <th className="p-3.5">Email Address</th>
              <th className="p-3.5 text-center">Status</th>
              <th className="p-3.5 text-center">Primary Recipient</th>
              <th className="p-3.5">Created Date</th>
              <th className="p-3.5 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850 text-xs font-semibold text-slate-350">
            {emails.map((item) => (
              <tr key={item.id} className="hover:bg-slate-950/10">
                <td className="p-3.5 text-slate-200 font-mono">{item.email_address}</td>
                <td className="p-3.5 text-center">
                  <button
                    onClick={() => onToggleStatus(item.id, !item.active)}
                    className={`px-2 py-0.5 rounded text-[9px] font-bold uppercase cursor-pointer border ${
                      item.active
                        ? 'bg-emerald-500/5 border-emerald-500/10 text-emerald-450'
                        : 'bg-slate-850 border-slate-800 text-slate-500'
                    }`}
                  >
                    {item.active ? 'Active' : 'Inactive'}
                  </button>
                </td>
                <td className="p-3.5 text-center">
                  <button
                    onClick={() => !item.primary && onSetPrimary(item.id)}
                    disabled={item.primary}
                    className={`inline-flex items-center space-x-1 px-2.5 py-0.5 rounded text-[9px] font-bold uppercase transition-all ${
                      item.primary
                        ? 'bg-purple-500/10 border border-purple-500/20 text-purple-400 cursor-default'
                        : 'bg-slate-850 hover:bg-slate-800 border border-slate-800 text-slate-500 cursor-pointer'
                    }`}
                  >
                    <Star className={`w-3 h-3 ${item.primary ? 'fill-purple-400 text-purple-400' : ''}`} />
                    <span>{item.primary ? 'Primary' : 'Set Primary'}</span>
                  </button>
                </td>
                <td className="p-3.5 text-slate-500 font-mono text-[11px]">
                  {new Date(item.created_at).toLocaleDateString()}
                </td>
                <td className="p-3.5 text-right">
                  <div className="flex items-center justify-end space-x-2.5">
                    <button
                      onClick={() => onEdit(item)}
                      className="p-1 hover:bg-slate-850 rounded text-slate-400 hover:text-slate-200 transition-colors cursor-pointer"
                      title="Edit Email"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => onDelete(item.id)}
                      className="p-1 hover:bg-rose-500/10 rounded text-slate-500 hover:text-rose-400 transition-colors cursor-pointer"
                      title="Delete Email"
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
