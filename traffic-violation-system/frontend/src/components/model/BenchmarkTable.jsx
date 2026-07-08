import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function BenchmarkTable({ benchmarks }) {
  if (!benchmarks || benchmarks.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-slate-950/60 text-[10px] text-slate-500 uppercase tracking-wider font-bold border-b border-slate-850">
            <th className="p-4">Benchmark Attribute</th>
            <th className="p-4">Current Run</th>
            <th className="p-4">Baseline Avg</th>
            <th className="p-4 text-right">Offset Ratio</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-850 text-xs font-semibold">
          {benchmarks.map((b, idx) => {
            const isNegative = b.difference_pct < 0;
            return (
              <tr key={idx} className="hover:bg-slate-950/20 text-slate-350">
                <td className="p-4 font-bold text-slate-200">{b.metric_name}</td>
                <td className="p-4 font-mono text-slate-400">{b.current_val}</td>
                <td className="p-4 font-mono text-slate-400">{b.average_val}</td>
                <td className="p-4 text-right flex items-center justify-end space-x-1.5 font-mono">
                  {isNegative ? (
                    <TrendingDown className="w-3.5 h-3.5 text-emerald-450" />
                  ) : (
                    <TrendingUp className="w-3.5 h-3.5 text-rose-450" />
                  )}
                  <span className={isNegative ? 'text-emerald-450' : 'text-rose-450'}>
                    {b.difference_pct.toFixed(1)}%
                  </span>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
