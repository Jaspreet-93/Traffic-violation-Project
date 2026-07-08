import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function AccuracyChart({ data }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Daily Processing Traffic Volumes</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis dataKey="date" stroke="#64748b" fontSize={10} />
            <YAxis stroke="#64748b" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }} />
            <Line type="monotone" dataKey="vehicles" stroke="#a855f7" strokeWidth={2.5} name="Vehicles" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
