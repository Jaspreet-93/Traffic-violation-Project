import React from 'react';

export default function TimelineBar({ progress, onChange }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex flex-col space-y-2">
      <div className="relative w-full h-1.5 bg-slate-955 rounded-full overflow-hidden border border-slate-850">
        <input
          type="range"
          min="0"
          max="100"
          value={progress}
          onChange={(e) => onChange(parseFloat(e.target.value))}
          className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
        />
        <div
          className="bg-purple-650 h-full rounded-full transition-all duration-100"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <div className="flex justify-between text-[10px] text-slate-500 font-mono">
        <span>00:00</span>
        <span>Progress: {progress.toFixed(0)}%</span>
        <span>Duration: 15.0s</span>
      </div>
    </div>
  );
}
