import React from 'react';
import { Shield, ShieldAlert, Cpu, Clock, Activity, BarChart3, AlertCircle } from 'lucide-react';

export default function AIOverviewCard({ overview }) {
  if (!overview) return null;

  const items = [
    {
      label: "System Health",
      value: overview.system_health,
      icon: overview.system_health === 'Healthy' ? Shield : ShieldAlert,
      color: overview.system_health === 'Healthy' ? "text-emerald-400" : "text-rose-450"
    },
    {
      label: "Model Operational status",
      value: `${overview.running_models} / ${overview.total_models} Running`,
      icon: Cpu,
      color: "text-purple-400"
    },
    {
      label: "Loaded Models count",
      value: `${overview.loaded_models} Loaded`,
      icon: Cpu,
      color: "text-purple-450"
    },
    {
      label: "System Uptime",
      value: overview.system_uptime,
      icon: Clock,
      color: "text-slate-450"
    },
    {
      label: "Average Confidence",
      value: `${(overview.average_confidence * 100).toFixed(0)}%`,
      icon: Activity,
      color: "text-sky-400"
    },
    {
      label: "Current FPS",
      value: `${overview.fps.toFixed(1)} FPS`,
      icon: BarChart3,
      color: "text-indigo-400"
    },
    {
      label: "Pipeline Status",
      value: overview.pipeline_status,
      icon: AlertCircle,
      color: "text-amber-400"
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {items.map((item, idx) => {
        const Icon = item.icon;
        return (
          <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-3 shadow-md">
            <div className={`p-2.5 rounded-lg ${item.color} bg-slate-950`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">{item.label}</span>
              <span className="text-sm font-bold text-slate-200 mt-0.5 block">{item.value}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
