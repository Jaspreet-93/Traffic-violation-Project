import React from 'react';
import { Target, TrendingUp, Info } from 'lucide-react';

export default function TrainingMetrics({ metrics }) {
  if (!metrics) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-center items-center text-center py-10">
        <Info className="w-10 h-10 text-slate-700 mb-2" />
        <h4 className="text-xs font-semibold text-slate-400">Training Metrics Not Available</h4>
        <p className="text-[10px] text-slate-600 mt-1">Local training log curves or Roboflow artifact metrics files are not present on this terminal.</p>
      </div>
    );
  }

  const items = [
    { label: "Precision", value: metrics.precision },
    { label: "Recall", value: metrics.recall },
    { label: "F1 Score", value: metrics.f1_score },
    { label: "mAP@50", value: metrics.map_50 },
    { label: "mAP@50-95", value: metrics.map_50_95 }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Target className="w-4.5 h-4.5 text-purple-400" />
        <span>Training Verification</span>
      </h3>

      <div className="space-y-4">
        {/* Dataset/Epoch summary */}
        <div className="bg-slate-950/60 border border-slate-850 p-3 rounded-lg text-xs leading-relaxed">
          <div className="flex justify-between">
            <span className="text-slate-500">Dataset Used</span>
            <span className="text-slate-350 font-medium truncate max-w-[200px]">{metrics.dataset_used}</span>
          </div>
          <div className="flex justify-between mt-1.5">
            <span className="text-slate-500">Epochs Trained</span>
            <span className="text-slate-350 font-bold font-mono">{metrics.epochs} Epochs</span>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {items.map((item, idx) => (
            <div key={idx} className="bg-slate-950 border border-slate-850 p-2.5 rounded-lg text-center text-xs">
              <span className="text-slate-500 block text-[10px] uppercase font-bold tracking-wider">{item.label}</span>
              <span className="text-sm font-bold text-slate-200 mt-1 block font-mono">{item.value.toFixed(4)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
