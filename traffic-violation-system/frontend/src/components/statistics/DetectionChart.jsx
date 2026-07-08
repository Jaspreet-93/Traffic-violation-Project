import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function DetectionChart({ data }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Monthly Infractions Trends</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis dataKey="month" stroke="#64748b" fontSize={10} />
            <YAxis stroke="#64748b" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }} />
            <Line type="monotone" dataKey="violations" stroke="#3b82f6" strokeWidth={2.5} name="Violations" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
