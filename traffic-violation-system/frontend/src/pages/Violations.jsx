import React, { useState, useEffect } from 'react';
import { Search, ShieldAlert, Calendar, Star, Eye, Trash2, Download, RefreshCw, ChevronLeft, ChevronRight, ArrowUpDown, FileText, Info } from 'lucide-react';
import { violationAPI, evidenceAPI } from '../services/api';
import EvidenceViewer from '../components/EvidenceViewer';

export default function Violations() {
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedViolationId, setSelectedViolationId] = useState(null);
  
  // Sorting & Pagination
  const [sortField, setSortField] = useState('timestamp');
  const [sortOrder, setSortOrder] = useState('desc');
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);
  
  // Modals / Details view
  const [detailItem, setDetailItem] = useState(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState(null);

  useEffect(() => {
    setCurrentPage(1);
  }, [search, filterType]);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchViolations();
    }, 200);

    return () => clearTimeout(delayDebounceFn);
  }, [currentPage, search, filterType]);

  const fetchViolations = async () => {
    try {
      setLoading(true);
      const res = await violationAPI.getAll(currentPage, itemsPerPage, search, filterType);
      setViolations(res.data);
    } catch (err) {
      console.error("Error loading violation records:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSort = (field) => {
    const isAsc = sortField === field && sortOrder === 'asc';
    setSortOrder(isAsc ? 'desc' : 'asc');
    setSortField(field);
  };

  const handleDelete = async (id) => {
    try {
      await violationAPI.delete(id);
      setViolations(prev => prev.filter(v => v.id !== id));
      setConfirmDeleteId(null);
    } catch (err) {
      console.error("Error deleting violation record:", err);
    }
  };

  // Advanced search logic
  const filtered = violations.filter(v => {
    const term = search.toLowerCase();
    
    // Support searching: Vehicle ID, Plate Number, Violation ID, Evidence ID, Violation Type, Camera, Date
    const matchesSearch = 
      String(v.vehicle_id).includes(term) ||
      String(v.id).includes(term) ||
      String(v.evidence_id).includes(term) ||
      (v.plate_number && v.plate_number.toLowerCase().includes(term)) ||
      (v.violation && v.violation.toLowerCase().includes(term)) ||
      (v.camera_id && v.camera_id.toLowerCase().includes(term)) ||
      (v.timestamp && v.timestamp.toLowerCase().includes(term));
      
    // Filters matching: All Violations, No Helmet, Seat Belt, Traffic Light, Speed, Wrong Lane, Mobile Phone, Triple Riding, Expired Registration
    let matchesFilter = true;
    if (filterType !== 'all') {
      const f = filterType.toLowerCase();
      const vType = v.violation ? v.violation.toLowerCase() : '';
      if (f === 'no helmet') matchesFilter = vType.includes('helmet');
      else if (f === 'seat belt') matchesFilter = vType.includes('seat') || vType.includes('belt');
      else if (f === 'traffic light') matchesFilter = vType.includes('light') || vType.includes('red');
      else if (f === 'speed') matchesFilter = vType.includes('speed');
      else if (f === 'wrong lane') matchesFilter = vType.includes('lane') || vType.includes('wrong');
      else if (f === 'mobile phone') matchesFilter = vType.includes('phone') || vType.includes('mobile');
      else if (f === 'triple riding') matchesFilter = vType.includes('triple') || vType.includes('riding');
      else if (f === 'expired registration') matchesFilter = vType.includes('expired') || vType.includes('registration');
      else matchesFilter = vType === f;
    }
    
    return matchesSearch && matchesFilter;
  });

  // Sorting logic
  const sorted = [...filtered].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];
    
    if (typeof aVal === 'string') {
      return sortOrder === 'asc' 
        ? aVal.localeCompare(bVal) 
        : bVal.localeCompare(aVal);
    } else {
      return sortOrder === 'asc' 
        ? (aVal || 0) - (bVal || 0)
        : (bVal || 0) - (aVal || 0);
    }
  });

  // Pagination logic
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = sorted.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(sorted.length / itemsPerPage);

  const handleExportCSV = async () => {
    try {
      // Fetch all records without page limit (e.g. limit=1000000) matching search & filter
      const res = await violationAPI.getAll(1, 1000000, search, filterType);
      const allRecords = res.data || [];
      if (allRecords.length === 0) return;

      const headers = ["Violation ID", "Vehicle ID", "Vehicle Type", "License Plate", "Violation Type", "Confidence", "Timestamp", "Camera ID", "Status"];
      const rows = allRecords.map(item => [
        item.id,
        item.vehicle_id,
        item.vehicle_type || 'car',
        item.plate_number || 'N/A',
        item.violation || 'N/A',
        item.confidence ? `${(item.confidence * 100).toFixed(1)}%` : 'N/A',
        item.timestamp || 'N/A',
        item.camera_id || 'N/A',
        item.status || 'Confirmed'
      ]);

      const csv = [headers, ...rows].map(r => r.map(val => `"${String(val).replace(/"/g, '""')}"`).join(",")).join("\n");
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `exported_violations_${new Date().toISOString().slice(0,10)}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch (err) {
      console.error("Failed to export violations to CSV:", err);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Violation Records</h2>
          <p className="text-xs text-slate-500">Search and audit all AI-identified vehicle infraction events.</p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Export CSV button */}
          <button
            onClick={handleExportCSV}
            className="bg-slate-900 border border-slate-800 p-2.5 rounded-xl text-slate-400 hover:text-white transition-all flex items-center justify-center cursor-pointer"
            title="Export all to CSV"
          >
            <Download className="w-4 h-4" />
          </button>

          {/* Refresh button */}
          <button
            onClick={fetchViolations}
            className="bg-slate-900 border border-slate-800 p-2.5 rounded-xl text-slate-400 hover:text-white transition-all flex items-center justify-center cursor-pointer"
            title="Refresh logs"
          >
            <RefreshCw className="w-4 h-4" />
          </button>

          {/* Search bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input
              type="text"
              placeholder="Search ID / Plate / Camera..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setCurrentPage(1);
              }}
              className="bg-slate-900 border border-slate-800 text-xs px-9 py-2.5 rounded-xl text-slate-350 focus:outline-none focus:border-purple-500 w-56"
            />
          </div>

          {/* Category filter dropdown */}
          <select
            value={filterType}
            onChange={(e) => {
              setFilterType(e.target.value);
              setCurrentPage(1);
            }}
            className="bg-slate-900 border border-slate-800 text-xs px-3 py-2.5 rounded-xl text-slate-350 focus:outline-none focus:border-purple-500 cursor-pointer"
          >
            <option value="all">All Violations</option>
            <option value="no helmet">No Helmet</option>
            <option value="seat belt">Seat Belt</option>
            <option value="traffic light">Traffic Light</option>
            <option value="speed">Speed</option>
            <option value="wrong lane">Wrong Lane</option>
            <option value="mobile phone">Mobile Phone</option>
            <option value="triple riding">Triple Riding</option>
            <option value="expired registration">Expired Registration</option>
          </select>
        </div>
      </div>

      {/* Database Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl flex flex-col justify-between min-h-[400px]">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-slate-450 uppercase font-semibold tracking-wider text-[10px]">
                <th onClick={() => handleSort('id')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Violation ID</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('vehicle_id')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Vehicle ID</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('vehicle_type')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Vehicle Type</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('plate_number')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>License Plate</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('violation')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Violation Type</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('confidence')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors text-center">
                  <div className="flex items-center justify-center space-x-1.5">
                    <span>Confidence</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('timestamp')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Timestamp</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('camera_id')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors">
                  <div className="flex items-center space-x-1.5">
                    <span>Camera</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th onClick={() => handleSort('status')} className="px-6 py-4 cursor-pointer hover:bg-slate-900 transition-colors text-center">
                  <div className="flex items-center justify-center space-x-1.5">
                    <span>Evidence Status</span>
                    <ArrowUpDown className="w-3 h-3 text-slate-500" />
                  </div>
                </th>
                <th className="px-6 py-4 text-center">
                  <div className="flex items-center justify-center space-x-1.5">
                    <span>Processing Status</span>
                  </div>
                </th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850 text-slate-300">
              {loading ? (
                <tr>
                  <td colSpan="11" className="px-6 py-20 text-center">
                    <div className="flex justify-center items-center">
                      <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
                    </div>
                  </td>
                </tr>
              ) : currentItems.length === 0 ? (
                <tr>
                  <td colSpan="11" className="px-6 py-20 text-center text-slate-500">
                    No violation records found matching your filters.
                  </td>
                </tr>
              ) : (
                currentItems.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-950/20 transition-colors">
                    <td className="px-6 py-4 font-mono font-bold text-slate-400">#{item.id}</td>
                    <td className="px-6 py-4 font-bold text-slate-100">#{item.vehicle_id}</td>
                    <td className="px-6 py-4 capitalize">{item.vehicle_type}</td>
                    <td className="px-6 py-4 font-mono font-bold text-amber-400 tracking-wider">{item.plate_number}</td>
                    <td className="px-6 py-4 font-semibold text-purple-400">{item.violation}</td>
                    <td className="px-6 py-4 text-center">
                      <div className="flex items-center justify-center space-x-1">
                        <Star className="w-3 h-3 text-amber-500" />
                        <span className="font-semibold font-mono">{(item.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 font-mono text-[11px] text-slate-400">{item.timestamp}</td>
                    <td className="px-6 py-4">{item.camera_id}</td>
                    <td className="px-6 py-4 text-center">
                      <span className="px-2 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 font-bold uppercase text-[9px] tracking-wide">
                        {item.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <span className="px-2 py-0.5 rounded bg-purple-500/10 border border-purple-500/25 text-purple-400 font-bold uppercase text-[9px] tracking-wide">
                        Completed
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end space-x-2">
                        <button
                          onClick={() => setDetailItem(item)}
                          className="p-1.5 bg-slate-950 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-slate-200 border border-slate-850/60 transition-all cursor-pointer"
                          title="View detail info"
                        >
                          <Info className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => setSelectedViolationId(item.id)}
                          className="p-1.5 bg-slate-950 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-slate-200 border border-slate-850/60 transition-all cursor-pointer"
                          title="Open Evidence"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                        <a
                          href={`/api/v1/evidence/download/original/${item.evidence_id || item.id}`}
                          className="p-1.5 bg-slate-950 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-slate-200 border border-slate-850/60 transition-all cursor-pointer"
                          title="Download Original Frame"
                        >
                          <Download className="w-3.5 h-3.5 text-slate-500" />
                        </a>
                        <a
                          href={`/api/v1/evidence/download/annotated/${item.evidence_id || item.id}`}
                          className="p-1.5 bg-slate-950 hover:bg-slate-850 rounded-lg text-slate-400 hover:text-slate-250 border border-slate-850/60 transition-all cursor-pointer"
                          title="Download Annotated Overlays"
                        >
                          <Download className="w-3.5 h-3.5" />
                        </a>
                        <button
                          onClick={() => setConfirmDeleteId(item.id)}
                          className="p-1.5 bg-slate-955 border border-slate-850 hover:bg-rose-500/10 text-slate-500 hover:text-rose-500 rounded-lg transition-all cursor-pointer"
                          title="Delete Record"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination controls */}
        {totalPages > 1 && (
          <div className="bg-slate-955 border-t border-slate-850 px-6 py-4 flex items-center justify-between">
            <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">
              Showing {indexOfFirstItem + 1}-{Math.min(indexOfLastItem, sorted.length)} of {sorted.length} events
            </span>
            <div className="flex items-center space-x-1.5">
              <button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="p-1.5 bg-slate-900 border border-slate-800 rounded-lg text-slate-400 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="text-xs font-mono font-bold text-slate-350 px-3 py-1 bg-slate-900 border border-slate-800 rounded-lg">
                {currentPage} / {totalPages}
              </span>
              <button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="p-1.5 bg-slate-900 border border-slate-800 rounded-lg text-slate-400 hover:text-white disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Confirmation Modal for delete */}
      {confirmDeleteId && (
        <div className="fixed inset-0 bg-slate-955/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-sm overflow-hidden shadow-2xl p-6 space-y-4">
            <div className="flex items-center space-x-3 text-rose-500">
              <ShieldAlert className="w-6 h-6" />
              <h3 className="font-bold text-base text-slate-100">Purge Infraction Record?</h3>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              This action cannot be undone. It will delete violation record #{confirmDeleteId} and all associated logs.
            </p>
            <div className="flex justify-end space-x-3 pt-2">
              <button
                onClick={() => setConfirmDeleteId(null)}
                className="px-4 py-2 bg-slate-955 border border-slate-850 hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded-xl text-xs font-semibold cursor-pointer transition-all"
              >
                Cancel
              </button>
              <button
                onClick={() => handleDelete(confirmDeleteId)}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl text-xs font-semibold cursor-pointer transition-all"
              >
                Purge Record
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Detail info Modal */}
      {detailItem && (
        <div className="fixed inset-0 bg-slate-955/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
            <div className="bg-slate-955 px-6 py-4 border-b border-slate-850 flex justify-between items-center">
              <div>
                <h3 className="font-bold text-base text-slate-100">Violation Audit Logs</h3>
                <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Record ID #{detailItem.id}</span>
              </div>
              <button onClick={() => setDetailItem(null)} className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-850 transition-all cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-6 space-y-4 overflow-y-auto">
              <div className="bg-slate-955 border border-slate-850 p-4 rounded-xl space-y-2.5 text-xs text-slate-400">
                <div className="flex justify-between">
                  <span className="text-slate-500">Camera Source</span>
                  <span className="text-slate-250 font-semibold">{detailItem.camera_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Vehicle ID</span>
                  <span className="text-slate-250 font-semibold">#{detailItem.vehicle_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Vehicle Class</span>
                  <span className="text-slate-250 font-semibold capitalize">{detailItem.vehicle_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">License Plate</span>
                  <span className="text-slate-250 font-semibold font-mono tracking-wider">{detailItem.plate_number}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Violation Type</span>
                  <span className="text-purple-400 font-semibold">{detailItem.violation}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Classifier Confidence</span>
                  <span className="text-amber-400 font-bold">{(detailItem.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Captured Timestamp</span>
                  <span className="text-slate-250 font-mono">{detailItem.timestamp}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Evidence ID</span>
                  <span className="text-slate-250 font-semibold">#{detailItem.evidence_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Processing status</span>
                  <span className="text-emerald-450 font-semibold uppercase">{detailItem.status}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal popup */}
      {selectedViolationId && (
        <EvidenceViewer
          violationId={selectedViolationId}
          onClose={() => setSelectedViolationId(null)}
        />
      )}
    </div>
  );
}
