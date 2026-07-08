import React from 'react';
import { Cpu } from 'lucide-react';

export default function PerformanceChart({ performance }) {
  if (!performance) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <Cpu className="w-4 h-4 text-purple-400" />
        <span>Hardware Resources Audit</span>
      </h3>

      <div className="space-y-3.5 text-xs font-semibold">
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">GPU Workload</span>
          <span className="font-mono text-slate-300">{performance.gpu_utilization_pct}%</span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Memory Allocation</span>
          <span className="font-mono text-slate-300">{performance.memory_utilization_pct}%</span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">I/O Disk Write speed</span>
          <span className="font-mono text-slate-300">{performance.disk_write_speed_mbps} MB/s</span>
        </div>
        <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
          <span className="text-slate-500">Overall System Uptime</span>
          <span className="font-mono text-purple-450">{performance.uptime_percentage}%</span>
        </div>
      </div>
    </div>
  );
}
