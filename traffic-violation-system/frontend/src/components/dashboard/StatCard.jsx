import React from 'react';

export default function StatCard({ title, value, icon: Icon, color, bg }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-4">
      <div className={`${bg} p-3 rounded-lg`}>
        <Icon className={`w-6 h-6 ${color}`} />
      </div>
      <div>
        <span className="text-xs text-slate-500 block">{title}</span>
        <span className="text-xl font-bold text-slate-100">{value}</span>
      </div>
    </div>
  );
}
