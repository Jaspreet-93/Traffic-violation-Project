import React from 'react';
import { Shield, ShieldAlert, Cpu, Camera, Clock, Activity, BarChart } from 'lucide-react';

export default function AIOverview({ overview }) {
  if (!overview) return null;

  const getHealthBadge = (health) => {
    if (health === 'Healthy') return 'bg-emerald-500/10 border-emerald-500/20 text-emerald-450';
    if (health === 'Warning') return 'bg-amber-500/10 border-amber-500/20 text-amber-450';
    return 'bg-rose-500/10 border-rose-500/20 text-rose-450';
  };

  const cards = [
    {
      title: "System Health",
      value: overview.system_health,
      icon: overview.system_health === 'Healthy' ? Shield : ShieldAlert,
      color: overview.system_health === 'Healthy' ? "text-emerald-400" : "text-rose-400",
      bg: overview.system_health === 'Healthy' ? "bg-emerald-500/5 border border-emerald-500/10" : "bg-rose-500/5 border border-rose-500/10"
    },
    {
      title: "Total Models",
      value: `${overview.running_models} / ${overview.total_models} Active`,
      icon: Cpu,
      color: "text-purple-400",
      bg: "bg-purple-500/5 border border-purple-500/10"
    },
    {
      title: "Average Confidence",
      value: `${(overview.average_confidence * 100).toFixed(0)}%`,
      icon: Activity,
      color: "text-sky-400",
      bg: "bg-sky-500/5 border border-sky-500/10"
    },
    {
      title: "Processing Frame Rate",
      value: `${overview.fps.toFixed(1)} FPS`,
      icon: BarChart,
      color: "text-indigo-400",
      bg: "bg-indigo-500/5 border border-indigo-500/10"
    },
    {
      title: "Infractions Logged Today",
      value: overview.violations_today,
      icon: ShieldAlert,
      color: "text-rose-400",
      bg: "bg-rose-500/5 border border-rose-500/10"
    },
    {
      title: "Cameras Active",
      value: overview.active_cameras,
      icon: Camera,
      color: "text-amber-400",
      bg: "bg-amber-500/5 border border-amber-500/10"
    },
    {
      title: "Server RAM Load",
      value: `${overview.ram_usage.toFixed(0)}%`,
      icon: Cpu,
      color: "text-cyan-400",
      bg: "bg-cyan-500/5 border border-cyan-500/10"
    },
    {
      title: "System Uptime",
      value: overview.system_uptime,
      icon: Clock,
      color: "text-slate-400",
      bg: "bg-slate-500/5 border border-slate-500/10"
    }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {cards.map((c, idx) => {
        const Icon = c.icon;
        return (
          <div key={idx} className={`bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-3.5 shadow`}>
            <div className={`p-2.5 rounded-lg ${c.color} bg-slate-950`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">{c.title}</span>
              <span className="text-sm font-bold text-slate-200 mt-0.5 block">{c.value}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
