import React from 'react';
import { Activity, ShieldCheck } from 'lucide-react';

export default function ConfidenceMonitor({ confidence }) {
  if (!confidence) return null;

  const items = [
    { label: 'Vehicle Detection', value: confidence.vehicle_detection, color: 'text-purple-400' },
    { label: 'Vehicle Tracking', value: confidence.vehicle_tracking, color: 'text-indigo-400' },
    { label: 'Helmet Detection', value: confidence.helmet_detection, color: 'text-cyan-400' },
    { label: 'Plate Detection', value: confidence.plate_detection, color: 'text-sky-400' },
    { label: 'License Plate OCR', value: confidence.ocr, color: 'text-teal-400' },
    { label: 'Seat Belt Status', value: confidence.seat_belt, color: 'text-amber-400' },
    { label: 'Traffic Signal Light', value: confidence.traffic_light, color: 'text-rose-400' },
    { label: 'Driver Behavior Check', value: confidence.driver_behavior, color: 'text-pink-400' },
    { label: 'Overall Violation Score', value: confidence.overall_violation, color: 'text-emerald-450', highlight: true }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-full justify-between">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Activity className="w-4.5 h-4.5 text-purple-400 animate-pulse" />
        <span>Live Confidence Monitor</span>
      </h3>

      <div className="space-y-3.5 flex-1 flex flex-col justify-around">
        {items.map((item, idx) => (
          <div
            key={idx}
            className={`flex items-center justify-between text-xs p-2 rounded-lg transition-all ${
              item.highlight
                ? 'bg-emerald-500/5 border border-emerald-500/10'
                : 'bg-slate-950/40 border border-slate-850'
            }`}
          >
            <span className="text-slate-450 font-medium">{item.label}</span>
            <div className="flex items-center space-x-1.5 font-bold">
              <span className={item.color}>{(item.value * 100).toFixed(0)}%</span>
              {item.value >= 0.90 && <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
