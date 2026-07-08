import React, { useState, useEffect } from 'react';
import { reportsAPI } from '../services/reportsApi';
import ReportGenerator from '../components/reports/ReportGenerator';
import ReportHistory from '../components/reports/ReportHistory';
import ExportButtons from '../components/reports/ExportButtons';

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const res = await reportsAPI.getAll();
      setReports(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleGenerate = async (data) => {
    try {
      await reportsAPI.generate(data);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await reportsAPI.delete(id);
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleQuickExport = async (format) => {
    try {
      await reportsAPI.generate({ report_type: 'daily', export_format: format });
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-555 text-xs">
        <span>Loading Reports Center...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Reports Center</h2>
        <p className="text-xs text-slate-500">Compile aggregated summaries, export infraction listings and verify analytics logs.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <ReportHistory items={reports} onDelete={handleDelete} />
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          <ReportGenerator onGenerate={handleGenerate} />
          <ExportButtons onExport={handleQuickExport} />
        </div>
      </div>
    </div>
  );
}
