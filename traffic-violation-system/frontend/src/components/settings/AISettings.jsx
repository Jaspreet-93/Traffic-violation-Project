import React from 'react';
import { Cpu } from 'lucide-react';

export default function AISettings({ settings, onChange }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h3 className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center space-x-1.5">
        <Cpu className="w-4 h-4 text-purple-400" />
        <span>AI Analytics Thresholds</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Confidence Threshold */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Inference Confidence Limit</label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            value={settings.ai_confidence_threshold || 0.75}
            onChange={(e) => onChange('ai_confidence_threshold', parseFloat(e.target.value))}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>

        {/* Detection Threshold */}
        <div className="space-y-1.5 text-xs">
          <label className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Object Detection Limit</label>
          <input
            type="number"
            step="0.05"
            min="0"
            max="1"
            value={settings.ai_detection_threshold || 0.50}
            onChange={(e) => onChange('ai_detection_threshold', parseFloat(e.target.value))}
            className="w-full px-3 py-2 bg-slate-950 border border-slate-850 focus:border-purple-500 text-slate-200 rounded-lg outline-none font-semibold"
          />
        </div>
      </div>
    </div>
  );
}
