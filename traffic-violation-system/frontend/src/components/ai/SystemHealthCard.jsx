import React from 'react';
import { HardDrive, Cpu, Activity } from 'lucide-react';

export default function SystemHealthCard({ overview }) {
  if (!overview) return null;

  const metrics = [
    { label: 'CPU Usage', value: overview.cpu_usage, color: 'bg-purple-500', text: 'text-purple-400', icon: Cpu },
    { label: 'RAM Load', value: overview.ram_usage, color: 'bg-indigo-500', text: 'text-indigo-400', icon: Activity },
    { label: 'Storage Volume', value: overview.storage_usage, color: 'bg-sky-500', text: 'text-sky-400', icon: HardDrive }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-full justify-between">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Cpu className="w-4.5 h-4.5 text-purple-400" />
        <span>Resource Capacity Load</span>
      </h3>

      <div className="space-y-4 flex-1 flex flex-col justify-around">
        {metrics.map((m, idx) => {
          const Icon = m.icon;
          return (
            <div key={idx} className="space-y-1.5">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-450 flex items-center space-x-1.5">
                  <Icon className="w-3.5 h-3.5" />
                  <span>{m.label}</span>
                </span>
                <span className={`font-bold ${m.text}`}>{m.value.toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-850">
                <div className={`${m.color} h-2 rounded-full`} style={{ width: `${m.value}%` }}></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
