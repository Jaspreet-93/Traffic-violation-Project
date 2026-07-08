import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Radio, Upload, AlertOctagon, FileVideo, BarChart3, Settings, Mail, Cpu, Activity, GitPullRequest, Video, FileText, ShieldCheck, User, LogOut } from 'lucide-react';

export default function Sidebar() {
  const navigate = useNavigate();
  const menuItems = [
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/live-monitoring', label: 'Live Monitoring', icon: Radio },
    { path: '/camera-management', label: 'Camera Management', icon: Video },
    { path: '/upload-detection', label: 'Upload Detection', icon: Upload },
    { path: '/violations', label: 'Violations', icon: AlertOctagon },
    { path: '/evidence-locker', label: 'Evidence Locker', icon: FileVideo },
    { path: '/ai-statistics', label: 'AI Statistics', icon: Activity },
    { path: '/model-verification', label: 'AI Verification', icon: ShieldCheck },
    { path: '/reports', label: 'Reports Center', icon: FileText },
    { path: '/analytics', label: 'Analytics Insights', icon: BarChart3 },
    { path: '/ai-command-center', label: 'AI Command Center', icon: Cpu },
    { path: '/confidence-dashboard', label: 'AI Confidence', icon: Activity },
    { path: '/ai-decision-engine', label: 'Decision Engine', icon: GitPullRequest },
    { path: '/replay-center', label: 'Replay Center', icon: Video },
    { path: '/profile', label: 'Edit Profile / PW', icon: User },
    { path: '/settings', label: 'System Settings', icon: Settings },
    { path: '/email-logs', label: 'Email Logs', icon: Mail },
  ];

  const handleLogout = () => {
    localStorage.removeItem('user_profile');
    localStorage.removeItem('admin_logged_in');
    navigate('/login');
  };

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-955 flex flex-col justify-between py-6 overflow-y-auto">
      <div className="space-y-6 px-4">
        <span className="text-[10px] font-bold text-slate-500 tracking-wider uppercase pl-2">Monitor Console</span>
        <div className="space-y-1">
          {menuItems.map((item, idx) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={idx}
                to={item.path}
                className={({ isActive }) =>
                  `w-full flex items-center space-x-3 px-4 py-2 rounded text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-purple-650 text-white shadow-lg shadow-purple-650/20'
                      : 'text-slate-450 hover:bg-slate-900 hover:text-slate-200'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </div>

      <div className="px-4 py-4 border-t border-slate-900 mt-6 space-y-3">
        <button
          onClick={handleLogout}
          className="w-full flex items-center space-x-3 px-4 py-2 rounded text-xs font-semibold text-rose-450 hover:bg-rose-500/5 transition-colors cursor-pointer"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout Session</span>
        </button>

        <div className="flex items-center space-x-2 text-[10px] text-slate-600 pl-2">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>AURA Engine v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
