import React from 'react';
import { Loader2 } from 'lucide-react';

export default function ProgressCard({ progress }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <div className="flex items-center justify-between text-xs font-semibold text-slate-200">
        <span className="flex items-center space-x-2">
          <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
          <span>Processing Video Job...</span>
        </span>
        <span className="text-purple-400 font-bold">{progress.toFixed(0)}%</span>
      </div>

      <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-850">
        <div
          className="bg-purple-650 h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      <p className="text-[10px] text-slate-550 leading-relaxed text-center font-medium">
        Running frame capture, YOLOv8 vehicle classifiers, ByteTrack tracker, and OCR models on uploaded footage. Please do not close this window.
      </p>
    </div>
  );
}
