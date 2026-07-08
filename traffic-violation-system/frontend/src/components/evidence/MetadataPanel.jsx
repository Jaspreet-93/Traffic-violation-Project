import React from 'react';
import { Info, Cpu } from 'lucide-react';

export default function MetadataPanel({ metadata }) {
  if (!metadata) return null;

  const items = [
    { label: 'Detection Time', value: metadata.detection_time, isMono: true },
    { label: 'Latency Duration', value: `${metadata.processing_time_ms} ms`, isMono: true },
    { label: 'Vehicle Class', value: metadata.vehicle_type },
    { label: 'Violation Type', value: metadata.violation_type, highlight: true },
    { label: 'Inference Confidence', value: `${(metadata.confidence * 100).toFixed(0)}%`, isMono: true },
    { label: 'AURA Version', value: metadata.model_version },
    { label: 'File Size', value: `${metadata.evidence_size_kb} KB`, isMono: true },
    { label: 'Resolution Dimensions', value: metadata.resolution, isMono: true }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Info className="w-4.5 h-4.5 text-purple-400" />
        <span>Hardware & File Metadata</span>
      </h3>

      <div className="space-y-3.5 text-xs font-semibold">
        {items.map((item, idx) => (
          <div key={idx} className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
            <span className="text-slate-500">{item.label}</span>
            <span className={`font-bold ${
              item.highlight ? 'text-rose-450' : item.isMono ? 'font-mono text-slate-350' : 'text-slate-250'
            }`}>
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
