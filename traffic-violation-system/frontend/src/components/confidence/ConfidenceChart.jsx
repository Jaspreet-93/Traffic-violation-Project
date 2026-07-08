import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function ConfidenceChart({ trend, avg }) {
  if (!trend || trend.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <TrendingUp className="w-4.5 h-4.5 text-purple-400" />
          <span>Surveillance Accuracy Trend</span>
        </h3>
        <span className="text-[10px] text-slate-400 font-bold bg-slate-950 px-2.5 py-1 rounded border border-slate-850">
          Avg: {avg}%
        </span>
      </div>

      <div className="h-[200px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trend} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="time" stroke="#64748b" fontSize={9} tickLine={false} />
            <YAxis stroke="#64748b" fontSize={9} tickLine={false} domain={[80, 100]} />
            <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '10px' }} />
            <Area type="monotone" dataKey="value" name="Confidence (%)" stroke="#aa3bff" fill="url(#confChartGlow)" strokeWidth={2} />
            <defs>
              <linearGradient id="confChartGlow" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#aa3bff" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#aa3bff" stopOpacity={0}/>
              </linearGradient>
            </defs>
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
