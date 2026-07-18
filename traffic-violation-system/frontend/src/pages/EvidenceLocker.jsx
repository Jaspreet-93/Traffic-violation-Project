import React, { useState, useEffect, useRef } from 'react';
import { evidenceAPI } from '../services/evidenceApi';
import EvidenceGrid from '../components/evidence/EvidenceGrid';
import FilterPanel from '../components/evidence/FilterPanel';
import EvidenceDetails from '../components/evidence/EvidenceDetails';

function EvidenceSkeleton() {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow animate-pulse flex flex-col h-72">
      <div className="h-40 bg-slate-850" />
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        <div className="space-y-2">
          <div className="h-3 bg-slate-800 rounded w-2/3" />
          <div className="h-2 bg-slate-800 rounded w-1/2" />
        </div>
        <div className="flex gap-2">
          <div className="h-7 bg-slate-800 rounded flex-1" />
          <div className="h-7 bg-slate-800 rounded w-8" />
        </div>
      </div>
    </div>
  );
}

export default function EvidenceLocker() {
  const [items, setItems] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [activeId, setActiveId] = useState(null);
  const [metadata, setMetadata] = useState(null);
  const [integrity, setIntegrity] = useState(null);
  const [search, setSearch] = useState('');
  const [filterClass, setFilterClass] = useState('All');
  const [loading, setLoading] = useState(true);
  
  // Selection & Bulk delete states
  const [selectedIds, setSelectedIds] = useState([]);
  const [deleteProgress, setDeleteProgress] = useState(null);
  const [showConfirmAll, setShowConfirmAll] = useState(false);
  const [confirmText, setConfirmText] = useState('');
  
  // Pagination & Infinite Scroll state
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);

  const abortControllerRef = useRef(null);

  const fetchEvidenceDetails = async (id) => {
    try {
      const [resDetail, resMeta, resInteg] = await Promise.all([
        evidenceAPI.getById(id),
        evidenceAPI.getMetadata(id),
        evidenceAPI.getIntegrity(id)
      ]);
      setMetadata({
        ...resDetail.data,
        ...resMeta.data
      });
      setIntegrity(resInteg.data);
    } catch (err) {
      console.error("Failed to load evidence inspect details:", err);
    }
  };

  const fetchEvidenceList = async (pageNum = 1) => {
    try {
      if (pageNum === 1) {
        setLoading(true);
      } else {
        setLoadingMore(true);
      }

      // Abort previous pending request if any
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      abortControllerRef.current = new AbortController();
      const signal = abortControllerRef.current.signal;

      let res;
      if (search.trim() || filterClass !== 'All') {
        const params = { page: pageNum, limit: 20 };
        if (search.trim()) {
          const q = search.trim();
          params.plate_number = q;
          params.violation_type = q;
          params.date = q;
          params.camera = q;
          if (!isNaN(q)) {
            params.evidence_id = parseInt(q);
            params.vehicle_id = parseInt(q);
          }
        }
        if (filterClass !== 'All') {
          params.violation_type = filterClass;
        }
        res = await evidenceAPI.search(params, { signal });
      } else {
        res = await evidenceAPI.getAll(pageNum, 20, { signal });
      }

      const raw = res.data || [];
      
      if (pageNum === 1) {
        setItems(raw);
        setFiltered(raw);
        
        if (raw.length > 0) {
          const exists = raw.some(item => item.evidence_id === activeId);
          if (!exists) {
            const firstId = raw[0].evidence_id;
            setActiveId(firstId);
            await fetchEvidenceDetails(firstId);
          }
        } else {
          setActiveId(null);
          setMetadata(null);
          setIntegrity(null);
        }
      } else {
        setItems(prev => {
          const seen = new Set(prev.map(p => p.evidence_id));
          const filteredRaw = raw.filter(r => !seen.has(r.evidence_id));
          return [...prev, ...filteredRaw];
        });
        setFiltered(prev => {
          const seen = new Set(prev.map(p => p.evidence_id));
          const filteredRaw = raw.filter(r => !seen.has(r.evidence_id));
          return [...prev, ...filteredRaw];
        });
      }

      if (raw.length < 20) {
        setHasMore(false);
      } else {
        setHasMore(true);
      }
    } catch (err) {
      if (err.name !== 'CanceledError' && err.message !== 'canceled') {
        console.error("Failed to list evidence logs:", err);
      }
    } finally {
      if (pageNum === 1) {
        setLoading(false);
      } else {
        setLoadingMore(false);
      }
    }
  };

  // Reset page and trigger fetch for page 1 on query search/filter updates
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      setPage(1);
      setHasMore(true);
      setSelectedIds([]);
      fetchEvidenceList(1);
    }, 200);

    return () => clearTimeout(delayDebounceFn);
  }, [search, filterClass]);

  // Load next pages automatically when state page changes
  useEffect(() => {
    if (page > 1) {
      fetchEvidenceList(page);
    }
  }, [page]);

  const handleScroll = (e) => {
    if (loading || loadingMore || !hasMore) return;
    const { scrollTop, clientHeight, scrollHeight } = e.currentTarget;
    // Trigger when scrolled to 90% of the container height
    if (scrollHeight - scrollTop <= clientHeight + 100) {
      setPage(prev => prev + 1);
    }
  };

  const handleSelect = async (id) => {
    setActiveId(id);
    setMetadata(null);
    setIntegrity(null);
    await fetchEvidenceDetails(id);
  };

  const handleToggleSelect = (id) => {
    setSelectedIds(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const handleSelectAll = () => {
    setSelectedIds(filtered.map(item => item.evidence_id));
  };

  const handleUnselectAll = () => {
    setSelectedIds([]);
  };

  const pollDeleteProgress = (jobId) => {
    const interval = setInterval(async () => {
      try {
        const res = await evidenceAPI.getBulkDeleteProgress(jobId);
        const { current, total, status } = res.data;
        setDeleteProgress({ current, total, status });
        
        if (status === 'completed' || status === 'failed') {
          clearInterval(interval);
          setTimeout(() => {
            setDeleteProgress(null);
            fetchEvidenceList(1);
          }, 1000);
        }
      } catch (err) {
        console.error("Error polling delete progress:", err);
        clearInterval(interval);
        setDeleteProgress(null);
      }
    }, 500);
  };

  const handleDeleteSelected = async () => {
    if (selectedIds.length === 0) return;
    try {
      const res = await evidenceAPI.deleteEvidenceBulk(selectedIds);
      const jobId = res.data.job_id;
      
      const updated = items.filter(item => !selectedIds.includes(item.evidence_id));
      setItems(updated);
      setFiltered(updated);
      setSelectedIds([]);
      
      if (updated.length > 0) {
        setActiveId(updated[0].evidence_id);
        fetchEvidenceDetails(updated[0].evidence_id);
      } else {
        setActiveId(null);
        setMetadata(null);
        setIntegrity(null);
      }
      
      setDeleteProgress({ current: 0, total: selectedIds.length, status: 'processing' });
      pollDeleteProgress(jobId);
    } catch (err) {
      console.error("Failed to bulk delete:", err);
    }
  };

  const handleDeleteAll = async () => {
    try {
      const res = await evidenceAPI.deleteAllEvidence();
      const jobId = res.data.job_id;
      
      setItems([]);
      setFiltered([]);
      setSelectedIds([]);
      setActiveId(null);
      setMetadata(null);
      setIntegrity(null);
      setShowConfirmAll(false);
      setConfirmText('');
      
      setDeleteProgress({ current: 0, total: items.length || 1, status: 'processing' });
      pollDeleteProgress(jobId);
    } catch (err) {
      console.error("Failed to delete all:", err);
    }
  };

  const handleExportSelected = () => {
    if (selectedIds.length === 0) return;
    const selectedItems = items.filter(item => selectedIds.includes(item.evidence_id));
    exportToCSV(selectedItems, `exported_evidence_${new Date().toISOString().slice(0,10)}.csv`);
  };

  const handleExportAll = () => {
    if (items.length === 0) return;
    exportToCSV(items, `all_evidence_${new Date().toISOString().slice(0,10)}.csv`);
  };

  const exportToCSV = (targetItems, filename) => {
    const headers = ["Evidence ID", "Violation ID", "Vehicle ID", "Plate Number", "Violation Type", "Timestamp", "Camera ID"];
    const rows = targetItems.map(item => [
      item.evidence_id,
      item.violation_id,
      item.vehicle_id || 'N/A',
      item.plate_number || 'N/A',
      item.violation || item.violation_type || 'N/A',
      item.timestamp || 'N/A',
      item.camera_id || 'N/A'
    ]);
    const csv = [headers, ...rows].map(r => r.map(val => `"${String(val).replace(/"/g, '""')}"`).join(",")).join("\n");
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleDelete = async (id) => {
    try {
      await evidenceAPI.deleteEvidence(id);
      const updated = items.filter(item => item.evidence_id !== id);
      setItems(updated);
      setFiltered(updated);
      setSelectedIds(prev => prev.filter(x => x !== id));
      if (updated.length > 0) {
        const nextId = updated[0].evidence_id;
        setActiveId(nextId);
        await fetchEvidenceDetails(nextId);
      } else {
        setActiveId(null);
        setMetadata(null);
        setIntegrity(null);
      }
    } catch (err) {
      console.error("Failed to delete evidence log:", err);
    }
  };

  return (
    <div 
      onScroll={handleScroll}
      className="flex-1 p-6 space-y-6 overflow-y-auto"
    >
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100 font-sans">Evidence Locker</h2>
        <p className="text-xs text-slate-500">Secure repository storing snapshots and raw recordings generated by the AI engine.</p>
      </div>

      {/* Filter panel */}
      <FilterPanel
        search={search}
        onSearchChange={setSearch}
        filterClass={filterClass}
        onFilterChange={setFilterClass}
      />

      {/* Selection Toolbar */}
      <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl flex flex-wrap gap-4 items-center justify-between text-xs text-slate-350">
        <div className="flex flex-wrap items-center gap-3">
          <button
            onClick={handleSelectAll}
            className="px-3 py-1.5 rounded bg-slate-955 hover:bg-slate-800 transition-all font-semibold flex items-center space-x-1 cursor-pointer border border-slate-850"
          >
            <span>☑ Select All</span>
          </button>
          <button
            onClick={handleUnselectAll}
            className="px-3 py-1.5 rounded bg-slate-955 hover:bg-slate-800 transition-all font-semibold flex items-center space-x-1 cursor-pointer border border-slate-850"
          >
            <span>☐ Unselect All</span>
          </button>
          
          <select
            onChange={(e) => {
              const val = e.target.value;
              if (val === 'images') {
                setSelectedIds(filtered.filter(item => !item.video_path).map(item => item.evidence_id));
              } else if (val === 'videos') {
                setSelectedIds(filtered.filter(item => item.video_path).map(item => item.evidence_id));
              } else if (val.startsWith('viol_')) {
                const vType = val.replace('viol_', '');
                setSelectedIds(filtered.filter(item => item.violation === vType).map(item => item.evidence_id));
              }
              e.target.value = '';
            }}
            className="bg-slate-955 border border-slate-850 text-slate-350 py-1.5 px-3 rounded focus:outline-none focus:border-purple-500 text-xs font-semibold cursor-pointer"
          >
            <option value="">Select by filter...</option>
            <option value="images">Images Only</option>
            <option value="videos">Videos Only</option>
            {Array.from(new Set(filtered.map(item => item.violation))).filter(Boolean).map(v => (
              <option key={v} value={`viol_${v}`}>Violation: {v}</option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-[10px] text-slate-500 font-bold space-x-3">
            <span>Selected: <span className="text-purple-400">{selectedIds.length}</span></span>
            <span>Filtered: <span className="text-slate-400">{filtered.length}</span></span>
            <span>Total: <span className="text-slate-400">{items.length}</span></span>
          </div>
          
          <button
            onClick={handleDeleteSelected}
            disabled={selectedIds.length === 0}
            className={`px-3 py-1.5 rounded font-bold transition-all flex items-center space-x-1 border border-slate-850 cursor-pointer ${
              selectedIds.length > 0 
                ? 'bg-rose-950/25 text-rose-400 hover:bg-rose-500/10 border-rose-500/20' 
                : 'bg-slate-955 text-slate-600 border-slate-900 cursor-not-allowed'
            }`}
          >
            <span>🗑 Delete Selected</span>
          </button>
          <button
            onClick={() => setShowConfirmAll(true)}
            className="px-3 py-1.5 rounded bg-rose-650 hover:bg-rose-700 text-white font-bold transition-all flex items-center space-x-1 cursor-pointer"
          >
            <span>🗑 Delete All</span>
          </button>
          <button
            onClick={handleExportSelected}
            disabled={selectedIds.length === 0}
            className={`px-3 py-1.5 rounded font-semibold transition-all flex items-center space-x-1 border border-slate-850 cursor-pointer ${
              selectedIds.length > 0 
                ? 'bg-slate-955 hover:bg-slate-800 text-slate-350' 
                : 'bg-slate-955 text-slate-655 border-slate-900 cursor-not-allowed'
            }`}
          >
            <span>⬇ Export Selected</span>
          </button>
          <button
            onClick={handleExportAll}
            disabled={items.length === 0}
            className={`px-3 py-1.5 rounded font-semibold transition-all flex items-center space-x-1 border border-slate-850 cursor-pointer ${
              items.length > 0 
                ? 'bg-slate-955 hover:bg-slate-800 text-slate-350' 
                : 'bg-slate-955 text-slate-655 border-slate-900 cursor-not-allowed'
            }`}
          >
            <span>⬇ Export All</span>
          </button>
          <button
            onClick={() => { fetchEvidenceList(1); setSelectedIds([]); }}
            className="px-3 py-1.5 rounded bg-slate-955 hover:bg-slate-800 text-slate-400 hover:text-white transition-all font-semibold flex items-center space-x-1 cursor-pointer border border-slate-850"
          >
            <span>🔄 Refresh</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Grid (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <EvidenceSkeleton key={i} />
              ))}
            </div>
          ) : (
            <>
              <EvidenceGrid
                items={filtered}
                onSelect={handleSelect}
                onDelete={handleDelete}
                selectedIds={selectedIds}
                onToggleSelect={handleToggleSelect}
              />
              
              {loadingMore && (
                <div className="flex justify-center py-4">
                  <span className="w-5 h-5 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
                </div>
              )}
            </>
          )}
        </div>

        {/* Right Panel (1 col) */}
        <div className="space-y-6">
          <EvidenceDetails
            activeId={activeId}
            metadata={metadata}
            integrity={integrity}
            onDelete={handleDelete}
          />
        </div>
      </div>

      {/* Delete All Confirmation Modal */}
      {showConfirmAll && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 max-w-md w-full rounded-2xl p-6 space-y-4 shadow-2xl animate-in fade-in zoom-in-95 duration-200">
            <h3 className="text-sm font-extrabold text-rose-500 uppercase tracking-wider">Delete ALL Evidence?</h3>
            <div className="space-y-2 text-xs text-slate-400">
              <p>This action will permanently delete:</p>
              <ul className="list-disc pl-5 space-y-1 text-slate-450">
                <li>Original Media</li>
                <li>Annotated Media</li>
                <li>Metadata</li>
                <li>OCR Data</li>
                <li>Thumbnails</li>
                <li>Database Records</li>
                <li>JSON Backup</li>
              </ul>
              <p className="text-[10px] text-slate-500 mt-2">This action cannot be undone.</p>
            </div>
            
            <div className="space-y-1.5">
              <label className="text-[10px] uppercase font-bold text-slate-400 block">Type DELETE to confirm:</label>
              <input
                type="text"
                placeholder="DELETE"
                value={confirmText}
                onChange={(e) => setConfirmText(e.target.value)}
                className="w-full bg-slate-955 border border-slate-850 py-2 px-3 rounded focus:outline-none focus:border-rose-500 text-xs text-slate-200 uppercase"
              />
            </div>
            
            <div className="flex justify-end gap-3 text-xs font-bold pt-2">
              <button
                onClick={() => { setShowConfirmAll(false); setConfirmText(''); }}
                className="px-4 py-2 rounded bg-slate-955 hover:bg-slate-800 text-slate-350 border border-slate-850 cursor-pointer"
              >
                Cancel
              </button>
              <button
                disabled={confirmText.toUpperCase() !== 'DELETE'}
                onClick={handleDeleteAll}
                className={`px-4 py-2 rounded font-bold text-white transition-all cursor-pointer ${
                  confirmText.toUpperCase() === 'DELETE'
                    ? 'bg-rose-600 hover:bg-rose-700'
                    : 'bg-slate-955 text-slate-650 border-slate-900 cursor-not-allowed'
                }`}
              >
                Delete Everything
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Delete Progress Modal */}
      {deleteProgress && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-sm p-4">
          <div className="bg-slate-900 border border-slate-800 max-w-sm w-full rounded-2xl p-6 space-y-4 shadow-2xl text-center">
            <h4 className="text-xs font-extrabold text-purple-400 uppercase tracking-wider">Deleting...</h4>
            
            <div className="w-full bg-slate-955 h-3 rounded-full overflow-hidden border border-slate-850">
              <div 
                className="bg-gradient-to-r from-purple-500 to-indigo-500 h-full rounded-full transition-all duration-300"
                style={{ width: `${Math.round((deleteProgress.current / deleteProgress.total) * 100) || 0}%` }}
              />
            </div>
            
            <div className="flex justify-between items-center text-[10px] text-slate-500 font-bold">
              <span>{Math.round((deleteProgress.current / deleteProgress.total) * 100) || 0}%</span>
              <span>Deleting {deleteProgress.current} / {deleteProgress.total}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
