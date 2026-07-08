import React from 'react';
import ReportGenerator from '../components/ai/ReportGenerator';

export default function Reports() {
  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Audit & Performance Reports</h2>
        <p className="text-xs text-slate-500">Compile and download historical health analysis report logs in PDF or Excel formats.</p>
      </div>

      <div className="max-w-2xl bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl">
        <ReportGenerator />
      </div>
    </div>
  );
}
