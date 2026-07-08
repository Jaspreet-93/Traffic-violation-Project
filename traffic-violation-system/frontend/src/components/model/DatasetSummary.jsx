import React from 'react';
import { Database } from 'lucide-react';

export default function DatasetSummary({ dataset }) {
  if (!dataset) return null;

  const items = [
    { label: 'Dataset Volume Name', value: dataset.dataset_name },
    { label: 'Storage Size', value: `${dataset.dataset_size_mb} MB`, isMono: true },
    { label: 'Total Snapshots', value: dataset.images_count, isMono: true },
    { label: 'Total Recordings', value: dataset.videos_count, isMono: true },
    { label: 'Total Classes', value: dataset.classes_count, isMono: true },
    { label: 'Total Annotations', value: dataset.annotations_count, isMono: true }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Database className="w-4.5 h-4.5 text-purple-400" />
        <span>Datasets Registry Audit</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-semibold">
        {items.map((item, idx) => (
          <div key={idx} className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-lg border border-slate-850">
            <span className="text-slate-500">{item.label}</span>
            <span className={item.isMono ? 'font-mono text-slate-350' : 'text-slate-250'}>
              {item.value}
            </span>
          </div>
        ))}
      </div>

      {/* Dataset Splits */}
      <div className="border-t border-slate-850 pt-4 space-y-3.5">
        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Training Split Partitions</span>
        <div className="flex bg-slate-955 border border-slate-850 p-1.5 rounded-lg text-xs font-mono font-semibold text-center text-slate-350">
          <div className="flex-1 border-r border-slate-850 py-1">Train: <span className="text-purple-400 font-bold">{(dataset.training_split * 100).toFixed(0)}%</span></div>
          <div className="flex-1 border-r border-slate-850 py-1">Val: <span className="text-purple-400 font-bold">{(dataset.validation_split * 100).toFixed(0)}%</span></div>
          <div className="flex-1 py-1">Test: <span className="text-purple-400 font-bold">{(dataset.test_split * 100).toFixed(0)}%</span></div>
        </div>
      </div>
    </div>
  );
}
