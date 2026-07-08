import React from 'react';
import { Eye, ShieldAlert, Cpu } from 'lucide-react';

export default function DetectionResult({ result }) {
  if (!result) return null;

  const outUrl = result.evidence.processed_file_url || '';
  const isVideo = result.file_type === 'video';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg space-y-4 p-5">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Cpu className="w-4 h-4 text-purple-400" />
        <span>Annotated AI Pipeline Outputs</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Media Canvas (2 cols) */}
        <div className="md:col-span-2 rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center min-h-[300px]">
          {isVideo ? (
            <video
              src={outUrl}
              controls
              className="w-full object-contain max-h-[400px]"
            />
          ) : (
            <img
              src={outUrl}
              alt="annotated-output"
              className="w-full object-contain max-h-[400px]"
            />
          )}
        </div>

        {/* Bboxes Audit Log (1 col) */}
        <div className="space-y-4">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">Detected Objects & Classes</span>
          <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
            {(!result.objects || result.objects.length === 0) ? (
              <div className="text-slate-550 text-xs text-center py-12">No objects detected.</div>
            ) : (
              result.objects.map((obj, idx) => (
                <div key={idx} className="bg-slate-955 border border-slate-850 p-2.5 rounded-lg flex flex-col space-y-1 text-xs">
                  <div className="flex justify-between items-center font-bold">
                    <span className="text-purple-400 capitalize">{obj.label}</span>
                    <span className="text-slate-250 font-mono">{(obj.confidence * 100).toFixed(0)}%</span>
                  </div>
                  <div className="text-[10px] text-slate-550 font-mono">
                    Bbox: [{obj.bbox.join(', ')}]
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
