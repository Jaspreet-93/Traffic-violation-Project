import React from 'react';
import { Info, Radio, Eye, ShieldAlert } from 'lucide-react';

export default function ReplayTelemetry({ info, timeline, frame, currentTimeOffset = 0, onEventClick }) {
  if (!info) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-500 text-xs">
        Select a footage item to load telemetry logs.
      </div>
    );
  }

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg p-5 space-y-5">
      {/* Title */}
      <div className="flex justify-between items-center text-xs border-b border-slate-850 pb-3">
        <h3 className="font-semibold text-slate-200 uppercase tracking-wider flex items-center space-x-2">
          <Info className="w-4 h-4 text-purple-400" />
          <span>Footage Telemetry Registry</span>
        </h3>
        <span className="text-[10px] text-purple-400 font-bold bg-slate-950 px-2.5 py-1 rounded border border-slate-850">
          ID: #{info.violation_id}
        </span>
      </div>

      {/* Info Specs */}
      <div className="grid grid-cols-2 gap-3 text-[10px] font-semibold">
        <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-850 space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block text-[8px]">Violation Type</span>
          <span className="text-rose-450 font-bold text-xs truncate block capitalize">{info.violation_type}</span>
        </div>
        <div className="bg-slate-955 p-2.5 rounded-lg border border-slate-850 space-y-1">
          <span className="text-slate-500 uppercase tracking-wider block text-[8px]">Confidence Score</span>
          <span className="text-purple-450 font-bold text-xs block font-mono">{info.overall_trust_score}%</span>
        </div>
        <div className="bg-slate-950/40 p-2.5 rounded-lg border border-slate-850 space-y-1 col-span-2">
          <span className="text-slate-500 uppercase tracking-wider block text-[8px]">Timestamp</span>
          <span className="text-slate-250 block font-mono">{info.timestamp}</span>
        </div>
      </div>

      {/* Timeline Events */}
      {timeline && timeline.length > 0 && (
        <div className="space-y-2 border-t border-slate-850 pt-3">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block flex items-center space-x-1.5">
            <Radio className="w-3.5 h-3.5 text-purple-400" />
            <span>Marked Infraction Events</span>
          </span>
          <div className="space-y-2 max-h-[160px] overflow-y-auto pr-1">
            {timeline.map((e, idx) => {
              const isPassed = e.time_offset_sec <= currentTimeOffset;
              return (
                <div
                  key={idx}
                  onClick={() => onEventClick && onEventClick(e.time_offset_sec)}
                  className={`flex items-start space-x-2 text-[10px] p-2 rounded-lg border transition-all cursor-pointer hover:border-purple-500/50 ${
                    isPassed
                      ? 'bg-purple-500/5 border-purple-500/20 text-slate-200'
                      : 'bg-slate-950/20 border-slate-850 text-slate-550'
                  }`}
                  title="Click to jump to event and resume"
                >
                  <span className="font-mono text-[9px] text-purple-400 mt-0.5 font-bold">{e.time_offset_sec.toFixed(1)}s</span>
                  <div className="space-y-0.5">
                    <div className="font-bold capitalize leading-tight">{e.event_name}</div>
                    <div className="text-[9px] text-slate-500 leading-normal">{e.description}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Selected Frame Diagnostics */}
      {frame && (
        <div className="space-y-2 border-t border-slate-850 pt-3">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block flex items-center space-x-1.5">
            <Eye className="w-3.5 h-3.5 text-purple-400" />
            <span>Active Frame Objects (Idx: {frame.frame_number})</span>
          </span>
          <div className="space-y-1.5 max-h-[140px] overflow-y-auto">
            {frame.objects.map((obj, idx) => (
              <div key={idx} className="bg-slate-950/40 border border-slate-850 p-2.5 rounded-lg flex justify-between items-center text-[10px] font-bold">
                <span className="text-purple-400 capitalize">{obj.label}</span>
                <span className="text-slate-250 font-mono">{(obj.confidence * 100).toFixed(0)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
