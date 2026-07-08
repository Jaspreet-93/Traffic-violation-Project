import React from 'react';
import { Gauge } from 'lucide-react';

export default function SpeedControl({ currentSpeed, onSpeedChange }) {
  const speeds = [0.25, 0.5, 1.0, 1.5, 2.0];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex items-center justify-between">
      <span className="text-xs text-slate-500 font-semibold flex items-center space-x-1.5">
        <Gauge className="w-4 h-4 text-purple-400" />
        <span>Playback Speed</span>
      </span>

      <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
        {speeds.map((s) => (
          <button
            key={s}
            onClick={() => onSpeedChange(s)}
            className={`px-2 py-1 rounded text-[10px] font-bold transition-all cursor-pointer ${
              currentSpeed === s ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            {s}x
          </button>
        ))}
      </div>
    </div>
  );
}
