import React, { useState, useEffect } from 'react';
import { reportsAPI } from '../services/reportsApi';
import ReportGenerator from '../components/reports/ReportGenerator';
import ReportHistory from '../components/reports/ReportHistory';
import ExportButtons from '../components/reports/ExportButtons';

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [toast, setToast] = useState(null);
  
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  const loadData = async (pageNum = 1) => {
    try {
      setLoading(true);
      const res = await reportsAPI.getAll(pageNum, 20);
      const sorted = (res.data || []).sort((a, b) => b.id - a.id);
      setReports(sorted);
      setHasMore(sorted.length === 20);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData(currentPage);
  }, [currentPage]);

  const handleGenerate = async (data) => {
    try {
      setGenerating(true);
      setToast(null);
      const res = await reportsAPI.generate(data);
      
      const newReportId = res.data?.report?.id;
      if (newReportId) {
        const downloadLink = document.createElement("a");
        downloadLink.href = `/api/v1/reports/${newReportId}`;
        downloadLink.download = `${res.data.report.name}.${data.export_format === 'excel' ? 'xlsx' : data.export_format}`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }

      await loadData(currentPage);
      setToast({
        type: 'success',
        message: res.data?.message || 'Report generated successfully!'
      });
      setTimeout(() => setToast(null), 4000);
    } catch (err) {
      console.error(err);
      setToast({
        type: 'error',
        message: 'Failed to generate report. Please try again.'
      });
      setTimeout(() => setToast(null), 4000);
    } finally {
      setGenerating(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      await reportsAPI.delete(id);
      await loadData(currentPage);
      setToast({
        type: 'success',
        message: 'Report log cleared successfully.'
      });
      setTimeout(() => setToast(null), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  const handleQuickExport = async (format) => {
    try {
      setGenerating(true);
      setToast(null);
      const res = await reportsAPI.generate({ report_type: 'daily', export_format: format });

      const newReportId = res.data?.report?.id;
      if (newReportId) {
        const downloadLink = document.createElement("a");
        downloadLink.href = `/api/v1/reports/${newReportId}`;
        downloadLink.download = `${res.data.report.name}.${format === 'excel' ? 'xlsx' : format}`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }

      await loadData(currentPage);
      setToast({
        type: 'success',
        message: res.data?.message || 'Report exported successfully!'
      });
      setTimeout(() => setToast(null), 4000);
    } catch (err) {
      console.error(err);
      setToast({
        type: 'error',
        message: 'Failed to export report. Please try again.'
      });
      setTimeout(() => setToast(null), 4000);
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-550 text-xs">
        <span className="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mb-2"></span>
        <span>Loading Reports Center...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto relative">
      {/* Toast Alert */}
      {toast && (
        <div className={`fixed top-4 right-4 z-50 flex items-center space-x-2.5 px-4 py-3 rounded-xl border text-xs font-bold shadow-xl animate-bounce ${
          toast.type === 'success' 
            ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400' 
            : 'bg-rose-500/10 border-rose-500/30 text-rose-400'
        }`}>
          <span className={`w-2 h-2 rounded-full shrink-0 ${toast.type === 'success' ? 'bg-emerald-400' : 'bg-rose-550'}`}></span>
          <span>{toast.message}</span>
        </div>
      )}

      <div>
        <h2 className="text-2xl font-bold text-slate-100">Reports Center</h2>
        <p className="text-xs text-slate-500">Compile aggregated summaries, export infraction listings and verify analytics logs.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <ReportHistory items={reports} onDelete={handleDelete} />
          
          {/* Pagination Footer */}
          <div className="flex items-center justify-between pt-4 border-t border-slate-850 text-xs">
            <button
              disabled={currentPage === 1 || loading}
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-40 disabled:hover:text-slate-450 disabled:cursor-not-allowed transition-all cursor-pointer"
            >
              Previous
            </button>
            <span className="text-slate-500 font-mono font-bold">Page {currentPage}</span>
            <button
              disabled={!hasMore || loading}
              onClick={() => setCurrentPage(prev => prev + 1)}
              className="px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white disabled:opacity-40 disabled:hover:text-slate-455 disabled:cursor-not-allowed transition-all cursor-pointer"
            >
              Next
            </button>
          </div>
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          <ReportGenerator onGenerate={handleGenerate} generating={generating} />
          <ExportButtons onExport={handleQuickExport} />
        </div>
      </div>
    </div>
  );
}
