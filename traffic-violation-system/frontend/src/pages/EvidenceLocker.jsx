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

  const handleDelete = async (id) => {
    try {
      await evidenceAPI.deleteEvidence(id);
      const updated = items.filter(item => item.evidence_id !== id);
      setItems(updated);
      setFiltered(updated);
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
    </div>
  );
}
