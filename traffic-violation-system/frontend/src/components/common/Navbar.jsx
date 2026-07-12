import React from 'react';
import { Shield, User, Menu } from 'lucide-react';
import { useSystem } from '../../context/SystemContext';

export default function Navbar({ onToggleSidebar }) {
  const { healthData } = useSystem();
  
  const status = healthData.status || 'Healthy';
  const displayStatus = status === 'Healthy' ? 'ONLINE' : status === 'Warning' ? 'WARNING' : 'OFFLINE';
  
  const badgeColor = status === 'Healthy' 
    ? 'bg-emerald-500' 
    : status === 'Warning' 
      ? 'bg-amber-500' 
      : 'bg-rose-500';
      
  const pingColor = status === 'Healthy' 
    ? 'bg-emerald-400' 
    : status === 'Warning' 
      ? 'bg-amber-400' 
      : 'bg-rose-400';

  return (
    <nav className="h-16 border-b border-slate-800 bg-slate-955/85 px-4 sm:px-6 flex items-center justify-between backdrop-blur-md sticky top-0 z-50">
      <div className="flex items-center space-x-3">
        <button
          onClick={onToggleSidebar}
          className="p-1.5 rounded-lg border border-slate-800 hover:bg-slate-900 text-slate-400 hover:text-slate-200 lg:hidden cursor-pointer"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="bg-purple-650/10 p-2 rounded-lg border border-purple-500/20 hidden sm:block">
          <Shield className="w-5 h-5 text-purple-400" />
        </div>
        <div>
          <span className="font-bold text-xs sm:text-sm bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent uppercase tracking-wider block sm:inline">
            AURA TRAFFIC MONITOR
          </span>
          <span className="text-[9px] text-slate-550 block">AI Infraction System</span>
        </div>
      </div>

      <div className="flex items-center space-x-2 sm:space-x-4">
        {/* Live System status indicator */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-850 px-3 py-1.5 rounded-full select-none">
          <span className="relative flex h-2 w-2">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${pingColor}`}></span>
            <span className={`relative inline-flex rounded-full h-2 w-2 ${badgeColor}`}></span>
          </span>
          <span className="text-[9px] sm:text-[10px] font-extrabold text-slate-400 whitespace-nowrap tracking-wider">
            {displayStatus}
          </span>
        </div>

        {/* User profile details */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-850 pl-2 pr-3 py-1 rounded-xl">
          <div className="bg-purple-650 p-1 rounded-lg text-white">
            <User className="w-3.5 h-3.5" />
          </div>
          <div className="text-left leading-none hidden sm:block">
            <span className="text-[10px] font-bold text-slate-200 block">Administrator</span>
            <span className="text-[8px] text-slate-500 uppercase tracking-wider font-semibold">Admin Panel</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
