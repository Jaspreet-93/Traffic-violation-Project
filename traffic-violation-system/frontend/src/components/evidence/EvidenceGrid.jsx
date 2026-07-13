import React from 'react';
import EvidenceCard from './EvidenceCard';
import { LayoutGrid } from 'lucide-react';

export default function EvidenceGrid({ items, onSelect, onDelete, selectedIds = [], onToggleSelect }) {
  if (!items || items.length === 0) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center shadow-md">
        <LayoutGrid className="w-8 h-8 text-slate-700 mx-auto mb-2" />
        <h4 className="text-xs font-semibold text-slate-400">No Evidence Found</h4>
        <p className="text-[10px] text-slate-650 mt-1">Locker registry is currently empty or filtered out.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {items.map((item) => (
        <EvidenceCard
          key={item.evidence_id}
          item={item}
          onSelect={onSelect}
          onDelete={onDelete}
          selected={selectedIds.includes(item.evidence_id)}
          onToggleSelect={onToggleSelect}
        />
      ))}
    </div>
  );
}
