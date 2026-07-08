import React from 'react';
import { BarChart3 } from 'lucide-react';

export default function MetricsCard({ metrics }) {
  if (!metrics) return null;

  const items = [
    { label: 'Precision Rating', value: metrics.precision, isFloat: true },
    { label: 'Recall Rating', value: metrics.recall, isFloat: true },
    { label: 'F1 Accuracy Score', value: metrics.f1_score, isFloat: true },
    { label: 'Model R2 score', value: metrics.r2_score, isFloat: true, highlight: true },
    { label: 'Mean Squared Error (MSE)', value: metrics.mean_squared_error, isFloat: true },
    { label: 'Mean Absolute Error (MAE)', value: metrics.mean_absolute_error, isFloat: true },
    { label: 'Mean AP @50', value: metrics.map_50, isFloat: true },
    { label: 'Mean AP @50-95', value: metrics.map_50_95, isFloat: true },
    { label: 'Avg Inference latency', value: `${metrics.inference_speed_ms} ms`, isMono: true },
    { label: 'Pipeline Speed', value: `${metrics.fps} FPS`, isMono: true },
    { label: 'RAM Memory Footprint', value: `${metrics.memory_usage_mb} MB`, isMono: true },
    { label: 'GPU load utilization', value: `${metrics.gpu_usage_pct}%`, isMono: true },
    { label: 'CPU load utilization', value: `${metrics.cpu_usage_pct}%`, isMono: true }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <BarChart3 className="w-4.5 h-4.5 text-purple-400" />
        <span>Validation Quality Indicators</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-semibold">
        {items.map((item, idx) => (
          <div key={idx} className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
            <span className="text-slate-500">{item.label}</span>
            <span className={`font-mono ${
              item.highlight ? 'text-purple-400 font-bold' : 'text-slate-300'
            }`}>
              {item.isFloat ? item.value.toFixed(2) : item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
