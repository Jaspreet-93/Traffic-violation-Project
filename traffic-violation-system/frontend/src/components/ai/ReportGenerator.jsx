import React, { useState } from 'react';
import { aiAPI } from '../../services/aiApi';
import { FileText, Download, CheckCircle, XCircle } from 'lucide-react';

export default function ReportGenerator() {
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState(null);

  const handleExport = async (format) => {
    try {
      setLoading(true);
      setMsg(null);
      const res = await aiAPI.exportReport(format);
      setMsg({ type: 'success', text: `Report exported successfully as ${format.toUpperCase()}! File saved under: ${res.data.report_file}` });
    } catch (err) {
      setMsg({ type: 'error', text: err.response?.data?.detail || err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <div>
        <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
          <FileText className="w-4.5 h-4.5 text-purple-400" />
          <span>Surveillance System Audit Reports</span>
        </h3>

        {msg && (
          <div className={`p-3 rounded-lg flex items-start space-x-2 text-xs font-semibold border mb-4 leading-relaxed ${
            msg.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450'
              : 'bg-rose-500/10 border-rose-500/20 text-rose-450'
          }`}>
            {msg.type === 'success' ? <CheckCircle className="w-4 h-4 mt-0.5" /> : <XCircle className="w-4 h-4 mt-0.5" />}
            <span className="break-all">{msg.text}</span>
          </div>
        )}

        <p className="text-xs text-slate-550 mb-6 leading-relaxed">
          Compile all validation audits, dataset counts, training precision curves, and hardware temperatures into a single file report.
        </p>
      </div>

      <div className="flex gap-4">
        <button
          onClick={() => handleExport('pdf')}
          disabled={loading}
          className="flex-1 bg-purple-650 hover:bg-purple-750 disabled:opacity-50 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs flex items-center justify-center space-x-1.5 cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export PDF</span>
        </button>

        <button
          onClick={() => handleExport('csv')}
          disabled={loading}
          className="flex-1 bg-slate-950 hover:bg-slate-950/80 border border-slate-800 disabled:opacity-50 text-slate-300 font-semibold py-2.5 rounded-xl transition-all text-xs flex items-center justify-center space-x-1.5 cursor-pointer"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export Excel/CSV</span>
        </button>
      </div>
    </div>
  );
}
