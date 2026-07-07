import React, { useState, useEffect } from 'react';
import { Search, ShieldAlert, Calendar, Star, Eye } from 'lucide-react';
import { violationAPI } from '../services/api';
import EvidenceViewer from '../components/EvidenceViewer';

export default function Violations() {
  const [violations, setViolations] = useState([]);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [selectedViolationId, setSelectedViolationId] = useState(null);

  useEffect(() => {
    fetchViolations();
  }, []);

  const fetchViolations = async () => {
    try {
      const res = await violationAPI.getAll();
      setViolations(res.data.reverse()); // latest first
    } catch (err) {
      console.error("Error loading violation records:", err);
    }
  };

  const filtered = violations.filter(v => {
    const matchesSearch = v.plate_number?.toLowerCase().includes(search.toLowerCase()) || 
                          String(v.vehicle_id).includes(search);
    const matchesFilter = filterType === 'all' || v.violation.toLowerCase() === filterType.toLowerCase();
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header & Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Violation Records</h2>
          <p className="text-xs text-slate-500">Search and audit all AI-identified vehicle infraction events.</p>
        </div>

        <div className="flex items-center space-x-3">
          {/* Search bar */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search ID / Plate..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="bg-slate-900 border border-slate-800 text-xs px-9 py-2.5 rounded-xl text-slate-350 focus:outline-none focus:border-purple-500 w-48"
            />
          </div>

          {/* Category filter */}
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="bg-slate-900 border border-slate-800 text-xs px-3 py-2.5 rounded-xl text-slate-350 focus:outline-none focus:border-purple-500 cursor-pointer"
          >
            <option value="all">All Violations</option>
            <option value="no helmet">No Helmet</option>
            <option value="no seatbelt">No Seatbelt</option>
            <option value="red light violation">Red Light</option>
            <option value="phone usage">Phone Usage</option>
            <option value="smoking">Smoking</option>
          </select>
        </div>
      </div>

      {/* Database Table */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="bg-slate-950 border-b border-slate-800 text-slate-450 uppercase font-semibold tracking-wider text-[10px]">
                <th className="px-6 py-4">Vehicle ID</th>
                <th className="px-6 py-4">License Plate</th>
                <th className="px-6 py-4">Infraction</th>
                <th className="px-6 py-4 text-center">Confidence</th>
                <th className="px-6 py-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850 text-slate-300">
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan="5" className="px-6 py-12 text-center text-slate-500">
                    No violation records found matching your filters.
                  </td>
                </tr>
              ) : (
                filtered.map((item, idx) => (
                  <tr key={idx} className="hover:bg-slate-950/20 transition-colors">
                    <td className="px-6 py-4 font-bold text-slate-100">#{item.vehicle_id}</td>
                    <td className="px-6 py-4 font-mono">{item.plate_number || 'PB10AB1234'}</td>
                    <td className="px-6 py-4">
                      <span className="font-semibold text-purple-400">{item.violation}</span>
                    </td>
                    <td className="px-6 py-4 text-center">
                      <div className="flex items-center justify-center space-x-1">
                        <Star className="w-3.5 h-3.5 text-amber-500" />
                        <span className="font-semibold">{(item.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => setSelectedViolationId(item.vehicle_id)} // search evidence by vehicle ID
                        className="inline-flex items-center space-x-1 text-purple-400 hover:text-purple-300 font-semibold transition-colors"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Evidence</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

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
