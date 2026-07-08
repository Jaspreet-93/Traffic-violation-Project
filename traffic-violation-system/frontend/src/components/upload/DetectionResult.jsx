import React from 'react';
import { ShieldAlert, Cpu, AlertTriangle } from 'lucide-react';

export default function DetectionResult({ result }) {
  if (!result) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col md:flex-row gap-6">
      {/* 1. Vehicle Details Card */}
      <div className="flex-1 space-y-4">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2 pb-2 border-b border-slate-800">
          <Cpu className="w-4 h-4 text-sky-400" />
          <span>Vehicle Details</span>
        </h3>
        
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <span className="text-slate-500 block uppercase font-bold tracking-wider text-[9px]">Vehicle Type</span>
            <span className="font-semibold text-slate-200 capitalize">{result.violations && result.violations.length > 0 ? "Motorcycle/Car" : "Car"}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase font-bold tracking-wider text-[9px]">Vehicle ID</span>
            <span className="font-semibold text-slate-200">#{result.vehicle_id}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase font-bold tracking-wider text-[9px]">License Plate</span>
            <span className="font-semibold text-purple-400 font-mono">{result.plate_number || 'PB10AB1234'}</span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase font-bold tracking-wider text-[9px]">Inference Confidence</span>
            <span className="font-semibold text-slate-200">{(result.confidence * 100).toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* 2. Violations Details Card */}
      <div className="flex-1 space-y-4">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2 pb-2 border-b border-slate-800">
          <ShieldAlert className="w-4.5 h-4.5 text-rose-500 animate-pulse" />
          <span>Detected Infractions</span>
        </h3>

        <div className="space-y-2">
          {(!result.violations || result.violations.length === 0) ? (
            <div className="text-slate-500 text-xs py-4 text-center">
              No traffic violations identified. Safe driving!
            </div>
          ) : (
            result.violations.map((violation, idx) => (
              <div key={idx} className="bg-slate-950 border border-slate-850 px-4 py-2.5 rounded-lg flex items-center justify-between text-xs">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-rose-500" />
                  <span className="font-bold text-slate-200">{violation}</span>
                </div>
                <span className="text-[10px] font-bold text-rose-400 bg-rose-500/5 px-2.5 py-0.5 rounded border border-rose-500/10 uppercase">
                  Infraction
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
