import React from 'react';
import { Loader2, CheckCircle2, Circle } from 'lucide-react';

export default function ProgressCard({ progress, jobStatus }) {
  const metrics = jobStatus?.metrics || {};

  const stages = [
    "Uploading",
    "Frame Extraction",
    "YOLO Detection",
    "Vehicle Tracking",
    "Violation Detection",
    "OCR",
    "Evidence Saving",
    "Database Update",
    "Completed"
  ];

  const currentStage = metrics.stage || (progress < 10 ? "Uploading" : "YOLO Detection");
  const currentIdx = stages.indexOf(currentStage);

  const getStepStatus = (stageName, idx) => {
    if (jobStatus?.status === 'Completed' || idx < currentIdx) return 'completed';
    if (idx === currentIdx && jobStatus?.status !== 'Completed') return 'active';
    return 'pending';
  };

  return (
    <div className="relative bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-6 shadow-2xl space-y-6 overflow-hidden">
      {/* Decorative neon gradient highlight */}
      <div className="absolute -top-24 -left-24 w-48 h-48 bg-purple-650/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-sky-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h4 className="text-xs font-bold text-slate-100 tracking-wide uppercase">AI Pipeline Execution</h4>
          <p className="text-[10px] text-slate-400">Footage is being processed frame-by-frame by YOLOv8 classifiers.</p>
        </div>
        <div className="flex items-center space-x-2 bg-purple-500/10 border border-purple-500/20 px-2.5 py-1 rounded-full">
          {jobStatus?.status !== 'Completed' && <Loader2 className="w-3 h-3 text-purple-400 animate-spin" />}
          <span className="text-[10px] text-purple-300 font-bold tracking-wider">{progress.toFixed(0)}%</span>
        </div>
      </div>

      {/* Progress Bar with Glow */}
      <div className="relative w-full bg-slate-950/60 rounded-full h-2.5 border border-slate-850/60 overflow-hidden">
        <div
          className="bg-gradient-to-r from-purple-600 via-indigo-500 to-sky-400 h-full rounded-full transition-all duration-300 shadow-[0_0_12px_rgba(139,92,246,0.4)]"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      {/* Pipeline Steps Checklist */}
      <div className="space-y-3 pt-2">
        <span className="text-[10px] font-bold text-slate-500 tracking-wider uppercase">Pipeline Stages</span>
        <div className="space-y-2">
          {stages.map((stageName, idx) => {
            const status = getStepStatus(stageName, idx);
            return (
              <div 
                key={idx} 
                className={`flex items-center justify-between p-2 rounded-lg border transition-all ${
                  status === 'active' 
                    ? 'bg-purple-500/5 border-purple-500/20 text-slate-200 shadow-sm'
                    : status === 'completed'
                    ? 'bg-slate-950/20 border-slate-850/30 text-slate-400'
                    : 'bg-slate-950/40 border-slate-900/50 text-slate-600'
                }`}
              >
                <div className="flex items-center space-x-3 text-xs font-semibold">
                  {status === 'completed' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0" />
                  ) : status === 'active' ? (
                    <Loader2 className="w-4 h-4 text-purple-400 animate-spin shrink-0" />
                  ) : (
                    <Circle className="w-4 h-4 text-slate-700 shrink-0" />
                  )}
                  <span className={status === 'active' ? 'text-purple-300 font-bold' : ''}>{stageName}</span>
                </div>
                <div className="text-[9px] font-mono tracking-wider uppercase">
                  {status === 'completed' && <span className="text-emerald-500 font-bold">Done</span>}
                  {status === 'active' && <span className="text-purple-400 font-bold animate-pulse">Running</span>}
                  {status === 'pending' && <span className="text-slate-600">Pending</span>}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Live Telemetry Panel */}
      <div className="space-y-3">
        <span className="text-[10px] font-bold text-slate-500 tracking-wider uppercase">Live Telemetry Metrics</span>
        <div className="grid grid-cols-3 gap-2 bg-slate-950/40 border border-slate-850/40 rounded-xl p-3 text-[10px] font-mono">
          <div className="space-y-0.5 text-center border-r border-slate-850/60">
            <div className="text-slate-500">SPEED</div>
            <div className="text-sky-400 font-bold">{metrics.current_fps || metrics.average_fps || 0} FPS</div>
          </div>
          <div className="space-y-0.5 text-center border-r border-slate-850/60">
            <div className="text-slate-500">FRAME</div>
            <div className="text-purple-400 font-bold">#{metrics.current_frame || 0} / {metrics.total_frames || 0}</div>
          </div>
          <div className="space-y-0.5 text-center">
            <div className="text-slate-500">HARDWARE</div>
            <div className="text-emerald-400 font-bold">{metrics.hardware || "CPU Core"}</div>
          </div>
        </div>

        {/* Detailed performance latency matrix */}
        <div className="grid grid-cols-2 gap-2 bg-slate-955/20 border border-slate-900/30 rounded-xl p-3 text-[9px] font-mono text-slate-400">
          <div className="flex justify-between border-b border-slate-900/40 pb-1">
            <span>Inference:</span>
            <span className="text-slate-200 font-bold">{metrics.detection_latency || 0} ms</span>
          </div>
          <div className="flex justify-between border-b border-slate-900/40 pb-1">
            <span>Tracking:</span>
            <span className="text-slate-200 font-bold">{metrics.tracking_latency || 0} ms</span>
          </div>
          <div className="flex justify-between border-b border-slate-900/40 pb-1">
            <span>OCR Latency:</span>
            <span className="text-slate-200 font-bold">{metrics.ocr_latency || 0} ms</span>
          </div>
          <div className="flex justify-between border-b border-slate-900/40 pb-1">
            <span>Evidence:</span>
            <span className="text-slate-200 font-bold">{metrics.evidence_latency || 0} ms</span>
          </div>
          <div className="flex justify-between">
            <span>CPU Usage:</span>
            <span className="text-slate-200 font-bold">{metrics.cpu_usage || 0}%</span>
          </div>
          <div className="flex justify-between">
            <span>Memory:</span>
            <span className="text-slate-200 font-bold">{metrics.memory_usage || 0}%</span>
          </div>
          <div className="flex justify-between">
            <span>Avg Frame:</span>
            <span className="text-slate-200 font-bold">{metrics.average_frame_time || 0} ms</span>
          </div>
          <div className="flex justify-between text-purple-400">
            <span>ETA Rem:</span>
            <span className="font-bold">{metrics.eta_remaining || 0}s</span>
          </div>
        </div>
      </div>
    </div>
  );
}
