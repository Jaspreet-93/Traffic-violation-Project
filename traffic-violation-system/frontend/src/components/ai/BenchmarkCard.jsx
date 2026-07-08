import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts';
import { Gauge } from 'lucide-react';

export default function BenchmarkCard({ benchmark }) {
  const COLORS = ['#aa3bff', '#6366f1', '#f43f5e', '#eab308'];

  if (!benchmark || benchmark.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Gauge className="w-4.5 h-4.5 text-purple-400" />
        <span>Performance Benchmark (Max Throughput)</span>
      </h3>

      <div className="h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={benchmark} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="model_name" stroke="#64748b" fontSize={9} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={9} tickLine={false} />
            <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '10px' }} />
            <Bar dataKey="max_throughput_fps" name="Max Capacity (FPS)" radius={[4, 4, 0, 0]}>
              {benchmark.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
