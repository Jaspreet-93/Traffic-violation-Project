import React from 'react';
import { Camera, Radio, Cpu, ShieldCheck, Mail, Database, ShieldAlert } from 'lucide-react';

export default function DecisionTimeline({ activeIndex = 11 }) {
  const steps = [
    { label: "Camera Frame Input", icon: Camera },
    { label: "Vehicle Detection Classifier", icon: Radio },
    { label: "Vehicle Frame Tracking", icon: Cpu },
    { label: "Helmet Presence Check", icon: ShieldAlert },
    { label: "License Plate Bbox", icon: Cpu },
    { label: "Characters OCR Recognition", icon: ShieldCheck },
    { label: "Seat Belt Check", icon: ShieldAlert },
    { label: "Signal Intersection Light Check", icon: Cpu },
    { label: "Driver Behaviour Scan", icon: Radio },
    { label: "Violation Decision Engine", icon: ShieldCheck },
    { label: "Evidence Report Generated", icon: Mail },
    { label: "DB Audit Storage Stored", icon: Database }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col justify-between h-full">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Cpu className="w-4.5 h-4.5 text-purple-400" />
        <span>Decision Flow Timeline</span>
      </h3>

      <div className="space-y-4">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          const isActive = idx <= activeIndex;
          return (
            <div key={idx} className="flex items-center space-x-3.5 text-xs">
              <div className={`p-2 rounded-full border transition-all ${
                isActive
                  ? 'bg-purple-500/10 border-purple-500/35 text-purple-400'
                  : 'bg-slate-950/40 border-slate-850 text-slate-600'
              }`}>
                <Icon className="w-3.5 h-3.5" />
              </div>
              <span className={`font-semibold ${isActive ? 'text-slate-200' : 'text-slate-650'}`}>
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
