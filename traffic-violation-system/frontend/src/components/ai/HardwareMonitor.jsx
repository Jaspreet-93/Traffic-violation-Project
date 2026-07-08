import React from 'react';
import { Cpu, Server, HardDrive, Shield } from 'lucide-react';

export default function HardwareMonitor({ hardware }) {
  if (!hardware) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Server className="w-4.5 h-4.5 text-purple-400" />
        <span>Hardware Diagnostics</span>
      </h3>

      <div className="space-y-4 flex-1 flex flex-col justify-around text-xs">
        {/* CPU Details */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <Cpu className="w-3.5 h-3.5" />
            <span>Processors</span>
          </span>
          <span className="font-bold text-slate-250 font-mono">{hardware.cpu_cores} Threads</span>
        </div>

        {/* Memory Details */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <Server className="w-3.5 h-3.5" />
            <span>Server RAM Size</span>
          </span>
          <span className="font-bold text-slate-250 font-mono">
            {hardware.ram_used_gb.toFixed(1)} / {hardware.ram_total_gb.toFixed(1)} GB
          </span>
        </div>

        {/* Disk Storage Details */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <HardDrive className="w-3.5 h-3.5" />
            <span>Disk Space</span>
          </span>
          <span className="font-bold text-slate-250 font-mono">
            {hardware.disk_used_gb.toFixed(0)} / {hardware.disk_total_gb.toFixed(0)} GB
          </span>
        </div>

        {/* Execution Device status */}
        <div className="flex justify-between items-center bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg">
          <span className="text-slate-500 flex items-center space-x-1.5">
            <Shield className="w-3.5 h-3.5" />
            <span>Execution Context</span>
          </span>
          <span className="font-bold text-slate-250 uppercase font-mono">
            {hardware.gpu_name || 'CPU (Standard)'}
          </span>
        </div>
      </div>
    </div>
  );
}
