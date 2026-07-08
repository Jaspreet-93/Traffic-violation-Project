import React from 'react';
import { Search, SlidersHorizontal } from 'lucide-react';

export default function FilterPanel({ search, onSearchChange, filterClass, onFilterChange }) {
  const classes = ["All", "No Helmet", "No Seat Belt", "Speed Limit Violation"];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow flex flex-col md:flex-row gap-4 items-center justify-between">
      {/* Search Input */}
      <div className="relative w-full md:w-80">
        <input
          type="text"
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search by Plate, ID..."
          className="w-full pl-9 pr-4 py-2.5 bg-slate-950 border border-slate-850 hover:border-slate-800 focus:border-purple-500 text-slate-200 text-xs font-semibold rounded-lg outline-none transition-all placeholder-slate-600"
        />
        <Search className="absolute left-3 top-3 w-4 h-4 text-slate-600" />
      </div>

      {/* Class filter buttons */}
      <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg w-full md:w-auto overflow-x-auto">
        {classes.map((c) => (
          <button
            key={c}
            onClick={() => onFilterChange(c)}
            className={`px-3 py-1.5 rounded text-[10px] font-bold uppercase transition-all whitespace-nowrap cursor-pointer ${
              filterClass === c ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            {c}
          </button>
        ))}
      </div>
    </div>
  );
}
