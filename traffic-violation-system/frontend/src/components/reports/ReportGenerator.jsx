import React, { useState } from 'react';
import { FileSpreadsheet, Plus } from 'lucide-react';

export default function ReportGenerator({ onGenerate, generating }) {
  const [type, setType] = useState('daily');
  const [format, setFormat] = useState('pdf');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (generating) return;
    onGenerate({ report_type: type, export_format: format });
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <FileSpreadsheet className="w-4 h-4 text-purple-400" />
        <span>Generate New Report</span>
      </h3>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Type select */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Report type</label>
          <select
            value={type}
            disabled={generating}
            onChange={(e) => setType(e.target.value)}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 text-xs font-semibold rounded-lg outline-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <option value="daily">Daily Summary Report</option>
            <option value="weekly">Weekly Infractions Report</option>
            <option value="monthly">Monthly Comparison Report</option>
            <option value="violation">Violation Log Details</option>
            <option value="camera">Camera Activity Report</option>
            <option value="ai_performance">AI Engine Inference Report</option>
          </select>
        </div>

        {/* Format select */}
        <div className="space-y-1.5">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Export Format</label>
          <select
            value={format}
            disabled={generating}
            onChange={(e) => setFormat(e.target.value)}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 text-xs font-semibold rounded-lg outline-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <option value="pdf">Adobe PDF (.pdf)</option>
            <option value="excel">Microsoft Excel (.xlsx)</option>
            <option value="csv">Standard CSV (.csv)</option>
          </select>
        </div>

        {/* Submit */}
        <button
          type="submit"
          disabled={generating}
          className="w-full bg-purple-650 hover:bg-purple-750 disabled:bg-slate-800 disabled:text-slate-500 text-white font-semibold py-2.5 rounded-lg text-xs flex items-center justify-center space-x-1 transition-all cursor-pointer disabled:cursor-not-allowed"
        >
          {generating ? (
            <>
              <span className="w-3.5 h-3.5 border-2 border-slate-500 border-t-transparent rounded-full animate-spin shrink-0"></span>
              <span>Compiling Report...</span>
            </>
          ) : (
            <>
              <Plus className="w-4 h-4" />
              <span>Generate Report</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
}
