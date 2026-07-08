import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function ConfidenceChart({ data }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Weekly Infractions Identified</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis dataKey="week" stroke="#64748b" fontSize={10} />
            <YAxis stroke="#64748b" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }} />
            <Bar dataKey="violations" fill="#ec4899" radius={[4, 4, 0, 0]} name="Violations" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
