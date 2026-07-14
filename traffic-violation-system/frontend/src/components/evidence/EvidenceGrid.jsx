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

  // Group items by date (day-wise)
  const groupedByDay = items.reduce((acc, item) => {
    let dateStr = "Unknown Date";
    if (item.timestamp) {
      const match = item.timestamp.match(/^\d{4}-\d{2}-\d{2}/);
      if (match) {
        dateStr = match[0];
      } else {
        dateStr = item.timestamp.split(' ')[0] || item.timestamp;
      }
    }
    
    let dayHeader = dateStr;
    try {
      const date = new Date(dateStr);
      if (!isNaN(date.getTime())) {
        dayHeader = date.toLocaleDateString(undefined, { 
          weekday: 'long', 
          year: 'numeric', 
          month: 'long', 
          day: 'numeric' 
        });
        
        const today = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        const yesterday = new Date(Date.now() - 86400000).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        
        const checkStr = date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
        if (checkStr === today) {
          dayHeader = `Today - ${dayHeader}`;
        } else if (checkStr === yesterday) {
          dayHeader = `Yesterday - ${dayHeader}`;
        }
      }
    } catch (e) {}

    if (!acc[dayHeader]) {
      acc[dayHeader] = [];
    }
    acc[dayHeader].push(item);
    return acc;
  }, {});

  return (
    <div className="space-y-8 animate-fadeIn">
      {Object.entries(groupedByDay).map(([dayHeader, dayItems]) => (
        <div key={dayHeader} className="space-y-4">
          <div className="flex items-center space-x-3 border-b border-slate-850/80 pb-2">
            <span className="w-1.5 h-4 bg-purple-500 rounded"></span>
            <h3 className="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 font-mono">
              {dayHeader}
            </h3>
            <span className="bg-slate-900 border border-slate-800 text-slate-500 font-mono px-2 py-0.5 rounded-full text-[9px] font-bold">
              {dayItems.length} {dayItems.length === 1 ? 'Record' : 'Records'}
            </span>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {dayItems.map((item) => (
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
        </div>
      ))}
    </div>
  );
}
