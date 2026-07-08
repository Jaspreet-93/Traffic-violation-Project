import React from 'react';
import { Eye, ShieldCheck } from 'lucide-react';

export default function FrameViewer({ frame }) {
  if (!frame) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Eye className="w-4.5 h-4.5 text-purple-400" />
        <span>Selected Frame Analysis</span>
      </h3>

      <div className="space-y-3.5 text-xs">
        <div className="flex justify-between items-center border-b border-slate-850 pb-2">
          <span className="text-slate-450 uppercase text-[9px] tracking-wider font-semibold">Frame Index</span>
          <span className="font-mono font-bold text-slate-350">{frame.frame_number}</span>
        </div>

        <div>
          <span className="text-[10px] text-slate-550 uppercase font-bold tracking-wider block mb-1">Detected Objects</span>
          <div className="space-y-2">
            {frame.objects.map((obj, idx) => (
              <div key={idx} className="bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg flex justify-between items-center font-bold">
                <span className="text-purple-400 capitalize">{obj.label}</span>
                <span className="text-slate-250 font-mono">{(obj.confidence * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
