import React from 'react';
import { Terminal, Shield, Mail, Video, Database } from 'lucide-react';

export default function SystemActivityLog() {
  const logs = [
    {
      id: 1,
      time: "Just Now",
      text: "Alert Dispatched: Violation email sent to officer list.",
      icon: Mail,
      color: "text-purple-400"
    },
    {
      id: 2,
      time: "3 mins ago",
      text: "North Intersection Camera signal: Online.",
      icon: Video,
      color: "text-emerald-400"
    },
    {
      id: 3,
      time: "10 mins ago",
      text: "YOLOv8 vehicle detection pipeline initialized.",
      icon: Shield,
      color: "text-indigo-400"
    },
    {
      id: 4,
      time: "25 mins ago",
      text: "Database backup: Sync completed successfully.",
      icon: Database,
      color: "text-slate-400"
    }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Terminal className="w-4.5 h-4.5 text-purple-400" />
        <span>System Activity Log</span>
      </h3>

      <div className="space-y-3">
        {logs.map((log) => {
          const Icon = log.icon;
          return (
            <div key={log.id} className="flex space-x-3 text-xs bg-slate-950/40 p-3 rounded-lg border border-slate-850">
              <div className={`p-1.5 rounded-lg bg-slate-900/60 ${log.color} flex-shrink-0`}>
                <Icon className="w-4 h-4" />
              </div>
              <div className="space-y-1">
                <p className="text-slate-250 font-semibold leading-normal">{log.text}</p>
                <span className="text-[10px] text-slate-550 block font-mono">{log.time}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
