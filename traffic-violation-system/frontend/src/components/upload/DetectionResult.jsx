import React, { useState } from 'react';
import { Eye, Cpu, Film, Image } from 'lucide-react';

export default function DetectionResult({ result }) {
  if (!result) return null;

  const isVideo = result.file_type === 'video';
  const [useOriginal, setUseOriginal] = useState(isVideo); // Default to original for video to ensure browser playback

  const originalUrl = `/uploads/${result.filename}`;
  const processedUrl = result.evidence.processed_file_url || '';
  const activeUrl = useOriginal ? originalUrl : processedUrl;

  // Filter out violation labels from the objects list as requested
  const violationLabels = ['no helmet', 'no seatbelt', 'no seat belt', 'phone usage', 'smoking', 'distracted', 'phone', 'behavior'];
  const filteredObjects = (result.objects || []).filter(
    (obj) => !violationLabels.includes(obj.label.toLowerCase())
  );

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg space-y-4 p-5">
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span>Annotated AI Pipeline Outputs</span>
        </h3>

        {/* Original vs Annotated toggle */}
        <div className="flex items-center bg-slate-950 border border-slate-850 p-1 rounded-lg">
          <button
            onClick={() => setUseOriginal(true)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
              useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setUseOriginal(false)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
              !useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Annotated
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Media Canvas (2 cols) */}
        <div className="md:col-span-2 space-y-4">
          <div className="rounded-lg overflow-hidden border border-slate-850 bg-slate-955 flex flex-col items-center justify-center min-h-[300px] relative">
            {isVideo ? (
              <video
                key={activeUrl}
                src={activeUrl}
                controls
                autoPlay
                muted
                className="w-full object-contain max-h-[400px]"
              />
            ) : (
              <img
                src={activeUrl}
                alt="annotated-output"
                className="w-full object-contain max-h-[400px]"
              />
            )}

            <div className="absolute top-3 left-3 bg-slate-950/80 border border-slate-850 text-slate-300 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
              {isVideo ? <Film className="w-3 h-3 text-purple-400" /> : <Image className="w-3 h-3 text-purple-400" />}
              <span>{useOriginal ? 'Original Video Stream' : 'AI Processed Overlay'}</span>
            </div>
          </div>

          {/* Captured Violation Proof Snapshot */}
          {isVideo && result.evidence.snapshot_url && (
            <div className="bg-slate-950 border border-slate-850 p-4 rounded-lg space-y-2">
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block flex items-center space-x-1.5">
                <Eye className="w-3.5 h-3.5 text-purple-400" />
                <span>Captured Violation Proof Screenshot</span>
              </span>
              <div className="rounded overflow-hidden border border-slate-850 bg-slate-955 flex justify-center max-h-[220px]">
                <img
                  src={result.evidence.snapshot_url}
                  alt="violation-proof"
                  className="w-full object-contain max-h-[220px]"
                />
              </div>
            </div>
          )}
        </div>

        {/* Bboxes Audit Log (1 col) */}
        <div className="space-y-4">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">Detected Objects & Classes</span>
          <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
            {filteredObjects.length === 0 ? (
              <div className="text-slate-550 text-xs text-center py-12">No objects detected.</div>
            ) : (
              filteredObjects.map((obj, idx) => (
                <div key={idx} className="bg-slate-955 border border-slate-850 p-2.5 rounded-lg flex justify-between items-center text-xs font-semibold">
                  <span className="text-purple-400 capitalize">{obj.label}</span>
                  <span className="text-slate-250 font-mono">{(obj.confidence * 100).toFixed(0)}%</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
