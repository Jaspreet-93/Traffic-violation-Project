import React from 'react';
import { Radio } from 'lucide-react';

export default function EventMarkers({ events, currentTimeOffset = 5.0 }) {
  if (!events || events.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Radio className="w-4.5 h-4.5 text-purple-400" />
        <span>Marked Infraction Events</span>
      </h3>

      <div className="space-y-3.5 max-h-[300px] overflow-y-auto pr-1">
        {events.map((e, idx) => {
          const isPassed = e.time_offset_sec <= currentTimeOffset;
          return (
            <div
              key={idx}
              className={`flex items-start space-x-3 text-xs p-2.5 rounded-lg border transition-all ${
                isPassed
                  ? 'bg-purple-500/5 border-purple-500/10 text-slate-200'
                  : 'bg-slate-950/20 border-slate-850 text-slate-550'
              }`}
            >
              <span className="font-mono text-[10px] text-purple-400 mt-0.5 font-bold">{e.time_offset_sec.toFixed(1)}s</span>
              <div className="space-y-0.5">
                <div className="font-bold capitalize">{e.event_name}</div>
                <div className="text-[10px] leading-relaxed text-slate-450">{e.description}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
