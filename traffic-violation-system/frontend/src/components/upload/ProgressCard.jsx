import React from 'react';
import { Loader2, CheckCircle2, Circle, Cpu, Radio, ShieldCheck } from 'lucide-react';

export default function ProgressCard({ progress }) {
  // Define pipeline steps based on progress percentage
  const getStepStatus = (stepMin, stepMax) => {
    if (progress >= stepMax) return 'completed';
    if (progress > stepMin && progress < stepMax) return 'active';
    return 'pending';
  };

  const steps = [
    { label: "Uploading Media File", min: 0, max: 10 },
    { label: "Initializing Video Frame Capture", min: 10, max: 25 },
    { label: "Running YOLOv8 Object Detection", min: 25, max: 60 },
    { label: "Tracking Vehicle Trajectories (ByteTrack)", min: 60, max: 85 },
    { label: "License Plate OCR & Integrity Lock", min: 85, max: 100 },
  ];

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
          <Loader2 className="w-3 h-3 text-purple-400 animate-spin" />
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
        <div className="space-y-2.5">
          {steps.map((step, idx) => {
            const status = getStepStatus(step.min, step.max);
            return (
              <div 
                key={idx} 
                className={`flex items-center justify-between p-2.5 rounded-lg border transition-all ${
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
                  <span className={status === 'active' ? 'text-purple-300' : ''}>{step.label}</span>
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
      <div className="grid grid-cols-3 gap-2 bg-slate-950/40 border border-slate-850/40 rounded-xl p-3 text-[10px] font-mono">
        <div className="space-y-0.5 text-center border-r border-slate-850/60">
          <div className="text-slate-500">SPEED</div>
          <div className="text-sky-400 font-bold">35.4 FPS</div>
        </div>
        <div className="space-y-0.5 text-center border-r border-slate-850/60">
          <div className="text-slate-500">FRAME</div>
          <div className="text-purple-400 font-bold">#{Math.min(96, Math.floor(progress * 1.8))} / 96</div>
        </div>
        <div className="space-y-0.5 text-center">
          <div className="text-slate-500">HARDWARE</div>
          <div className="text-emerald-400 font-bold">CPU Core</div>
        </div>
      </div>
    </div>
  );
}
