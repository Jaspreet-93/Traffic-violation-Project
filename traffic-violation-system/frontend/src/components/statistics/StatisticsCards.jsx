import React from 'react';

export default function StatisticsCards({ stats }) {
  if (!stats) return null;

  const items = [
    { label: 'Total Vehicles', value: stats.total_vehicles, color: 'text-purple-400' },
    { label: 'Total Violations', value: stats.total_violations, color: 'text-rose-400' },
    { label: 'Accuracy Rating', value: `${stats.detection_accuracy_pct}%`, color: 'text-emerald-400' },
    { label: 'Average Confidence', value: `${stats.avg_confidence_pct}%`, color: 'text-sky-400' },
    { label: 'Avg Inference Speed', value: `${stats.avg_inference_time_ms} ms`, color: 'text-amber-400' },
    { label: 'Pipeline Speed', value: `${stats.avg_detection_speed_fps} FPS`, color: 'text-indigo-400' }
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
      {items.map((item, idx) => (
        <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow flex flex-col justify-between space-y-2">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">{item.label}</span>
          <span className={`text-2xl font-bold font-mono ${item.color}`}>{item.value}</span>
        </div>
      ))}
    </div>
  );
}
