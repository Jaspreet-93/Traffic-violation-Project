import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function PerformanceCharts({ performance }) {
  if (!performance) return null;

  // Format array to chart metrics list
  const data = performance.precision_trend.map((p, idx) => ({
    epoch: `Epoch ${idx + 1}`,
    precision: p,
    recall: performance.recall_trend[idx],
    mAP: performance.map_trend[idx]
  }));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider">AI Training Convergence Metrics</h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis dataKey="epoch" stroke="#64748b" fontSize={10} />
            <YAxis stroke="#64748b" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc' }} />
            <Line type="monotone" dataKey="precision" stroke="#a855f7" strokeWidth={2.5} name="Precision" />
            <Line type="monotone" dataKey="recall" stroke="#ec4899" strokeWidth={2.5} name="Recall" />
            <Line type="monotone" dataKey="mAP" stroke="#3b82f6" strokeWidth={2.5} name="mAP@50" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
