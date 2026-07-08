import React from 'react';
import { Camera, CheckCircle, XCircle } from 'lucide-react';

export default function CameraStatusCard({ overview }) {
  const activeCount = overview?.active_cameras || 0;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Camera className="w-4.5 h-4.5 text-purple-400" />
        <span>Intersection Camera Feed Status</span>
      </h3>

      <div className="bg-slate-950 border border-slate-850 p-4 rounded-xl flex items-center justify-between text-xs">
        <div className="space-y-1">
          <span className="font-bold text-slate-200 block">Surveillance Stream #1</span>
          <span className="text-[10px] text-slate-500 font-mono">Channel: Local RTSP/Camera Loop</span>
        </div>
        
        {activeCount > 0 ? (
          <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded text-emerald-450 text-[10px] font-bold uppercase">
            <CheckCircle className="w-3.5 h-3.5" />
            <span>Active</span>
          </div>
        ) : (
          <div className="flex items-center space-x-1.5 bg-rose-500/10 border border-rose-500/20 px-2.5 py-1 rounded text-rose-450 text-[10px] font-bold uppercase">
            <XCircle className="w-3.5 h-3.5" />
            <span>Inactive</span>
          </div>
        )}
      </div>

      <div className="mt-4 flex justify-between text-[11px] text-slate-500 font-mono">
        <span>Active Feeds: {activeCount}</span>
        <span>Resolution: 1920x1080</span>
      </div>
    </div>
  );
}
