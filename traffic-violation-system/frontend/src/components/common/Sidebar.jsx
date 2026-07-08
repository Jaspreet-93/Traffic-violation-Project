import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Radio, Upload, AlertOctagon, FileVideo, BarChart3, Settings, Mail, Cpu, Activity, GitPullRequest, Video } from 'lucide-react';

export default function Sidebar() {
  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/live-monitoring', label: 'Live Monitoring', icon: Radio },
    { path: '/upload-detection', label: 'Upload Detection', icon: Upload },
    { path: '/violations', label: 'Violations', icon: AlertOctagon },
    { path: '/evidence-locker', label: 'Evidence Locker', icon: FileVideo },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/ai-command-center', label: 'AI Command Center', icon: Cpu },
    { path: '/confidence-dashboard', label: 'AI Confidence', icon: Activity },
    { path: '/ai-decision-engine', label: 'Decision Engine', icon: GitPullRequest },
    { path: '/replay-center', label: 'Replay Center', icon: Video },
    { path: '/settings', label: 'Email Settings', icon: Settings },
    { path: '/email-logs', label: 'Email Logs', icon: Mail },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col justify-between py-6 overflow-y-auto">
      <div className="space-y-6 px-4">
        <span className="text-xs font-bold text-slate-555 tracking-wider uppercase pl-2">Monitor Console</span>
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `w-full flex items-center space-x-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-purple-650 text-white shadow-lg shadow-purple-650/20'
                      : 'text-slate-450 hover:bg-slate-900 hover:text-slate-200'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </div>

      <div className="px-6 py-4 border-t border-slate-900 mt-6">
        <div className="flex items-center space-x-2 text-xs text-slate-555">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>AURA Engine v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
