import React from 'react';
import { ArrowRight, HelpCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function PipelineMonitor({ models, overview }) {
  // Map models config to stages for rendering
  const stages = [
    { name: "Camera Feed", status: "Healthy", time: 1.2, conf: 1.0 },
    { name: "Vehicle Detection", status: "Healthy", modelKey: "YOLOv8 Vehicle Detector" },
    { name: "Vehicle Tracking", status: "Healthy", modelKey: "ByteTrack Tracker" },
    { name: "Helmet Detection", status: "Healthy", modelKey: "Custom Helmet Detector" },
    { name: "Number Plate Detection", status: "Healthy", modelKey: "License Plate Detector" },
    { name: "License Plate OCR", status: "Healthy", modelKey: "License Plate OCR" },
    { name: "Seat Belt Detection", status: "Healthy", modelKey: "Seat Belt Detector" },
    { name: "Traffic Light Detection", status: "Healthy", modelKey: "Traffic Light Detector" },
    { name: "Driver Behaviour Detection", status: "Healthy", modelKey: "Driver Behavior Detector" },
    { name: "Violation Decision Engine", status: "Healthy", time: 0.5, conf: 1.0 },
    { name: "Evidence Generation", status: "Healthy", time: 15.0, conf: 1.0 },
    { name: "Email Notification", status: overview?.offline_models > 0 ? "Warning" : "Healthy", time: 45.0, conf: 1.0 },
    { name: "Officer Dashboard", status: "Healthy", time: 1.0, conf: 1.0 }
  ];

  const getStageStatus = (stage) => {
    if (stage.modelKey && models) {
      const match = models.find(m => m.name === stage.modelKey);
      if (match) {
        return {
          status: match.status === 'Running' ? 'Healthy' : 'Offline',
          time: match.inference_time,
          conf: match.confidence
        };
      }
    }
    return {
      status: stage.status,
      time: stage.time || 0.0,
      conf: stage.conf || 0.94
    };
  };

  const getStatusIcon = (status) => {
    if (status === 'Healthy') return <ShieldCheck className="w-4 h-4 text-emerald-500" />;
    if (status === 'Warning') return <AlertTriangle className="w-4 h-4 text-amber-500" />;
    return <AlertTriangle className="w-4 h-4 text-rose-500" />;
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <HelpCircle className="w-4.5 h-4.5 text-purple-400" />
        <span>Live Pipeline Execution Flow</span>
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {stages.map((stage, idx) => {
          const metrics = getStageStatus(stage);
          return (
            <div key={idx} className="bg-slate-950 border border-slate-850 p-3 rounded-lg flex flex-col justify-between text-xs space-y-2 relative group hover:border-purple-500/30 transition-all">
              <div className="flex items-center justify-between">
                <span className="font-bold text-slate-350">{stage.name}</span>
                {getStatusIcon(metrics.status)}
              </div>
              <div className="flex justify-between text-[10px] text-slate-500 font-mono">
                <span>Latency: {metrics.time.toFixed(1)}ms</span>
                <span>Conf: {(metrics.conf * 100).toFixed(0)}%</span>
              </div>
              {idx < stages.length - 1 && (
                <div className="hidden lg:block absolute -right-3.5 top-1/2 -translate-y-1/2 z-10 text-slate-700 group-hover:text-purple-500 transition-colors">
                  <ArrowRight className="w-3.5 h-3.5" />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
