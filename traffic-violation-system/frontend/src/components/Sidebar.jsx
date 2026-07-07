import React from 'react';
import { LayoutDashboard, AlertOctagon, FileVideo, BarChart3 } from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'violations', label: 'Violations', icon: AlertOctagon },
    { id: 'evidence', label: 'Evidence Vault', icon: FileVideo },
    { id: 'analytics', label: 'Analytics Insights', icon: BarChart3 },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950 flex flex-col justify-between py-6">
      <div className="space-y-6 px-4">
        <span className="text-xs font-semibold text-slate-500 tracking-wider uppercase">Monitor Console</span>
        <div className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-purple-650 text-white shadow-lg shadow-purple-650/20'
                    : 'text-slate-450 hover:bg-slate-900 hover:text-slate-200'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-slate-450'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      <div className="px-6 py-4 border-t border-slate-900">
        <div className="flex items-center space-x-2 text-xs text-slate-500">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>AURA Engine v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
