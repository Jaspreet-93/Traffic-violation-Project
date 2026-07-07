import React from 'react';
import { Shield, Radio, Activity } from 'lucide-react';

export default function Navbar({ cameraActive }) {
  return (
    <nav className="h-16 border-b border-slate-800 bg-slate-950/80 px-6 flex items-center justify-between backdrop-blur-md sticky top-0 z-50">
      <div className="flex items-center space-x-3">
        <div className="bg-purple-600/10 p-2 rounded-lg border border-purple-500/20">
          <Shield className="w-6 h-6 text-purple-500" />
        </div>
        <div>
          <span className="font-bold text-lg bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
            AURA TRAFFIC VIOLATION SYSTEM
          </span>
          <span className="text-xs text-slate-500 block">Real-time AI Infraction Monitor</span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        {/* Stream Status indicator */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-850 px-3 py-1.5 rounded-full">
          <span className="relative flex h-2.5 w-2.5">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${cameraActive ? 'bg-emerald-400' : 'bg-rose-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${cameraActive ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
          </span>
          <span className="text-xs font-semibold text-slate-300">
            {cameraActive ? 'LIVE CAMERA ACTIVE' : 'STREAM DISCONNECTED'}
          </span>
        </div>

        {/* System Latency Placeholder */}
        <div className="flex items-center space-x-2 text-slate-400 text-xs">
          <Activity className="w-4 h-4 text-purple-400" />
          <span>FPS: 15.2</span>
        </div>
      </div>
    </nav>
  );
}
