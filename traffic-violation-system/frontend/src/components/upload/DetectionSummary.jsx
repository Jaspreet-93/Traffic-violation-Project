import React, { useState, useEffect } from 'react';
import { ShieldCheck, Clock, ShieldAlert, FileText, BarChart2 } from 'lucide-react';

export default function DetectionSummary({ result }) {
  const [evidenceList, setEvidenceList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadEvidence() {
      if (!result || !result.filename) return;
      try {
        setLoading(true);
        const res = await fetch('/api/v1/evidence');
        if (res.ok) {
          const data = await res.json();
          // Filter matching the result.filename basename
          const matched = data.filter(item => {
            const fileBasename = decodeURIComponent(result.filename).toLowerCase();
            const paths = [
              item.original_image_path,
              item.annotated_image_path,
              item.original_video_path,
              item.annotated_video_path,
              item.image_path,
              item.video_path
            ].map(p => p ? decodeURIComponent(p).toLowerCase() : '');
            return paths.some(p => p.includes(fileBasename) || fileBasename.includes(p));
          });
          setEvidenceList(matched);
        }
      } catch (err) {
        console.error("Failed to load evidence for summary:", err);
      } finally {
        setLoading(false);
      }
    }
    loadEvidence();
  }, [result]);

  if (!result) return null;
  const evidence = result.evidence || {};

  // Count every violation type separately
  const violationCounts = {
    "No Helmet": 0,
    "Seat Belt": 0,
    "Triple Riding": 0,
    "Mobile Phone": 0,
    "Speed": 0,
    "Red Light": 0,
    "Wrong Lane": 0,
    "Stop Line": 0,
    "Parking": 0,
    "Number Plate": 0
  };

  evidenceList.forEach(item => {
    const v = item.violation ? item.violation.toLowerCase() : '';
    if (v.includes('helmet')) violationCounts["No Helmet"] += 1;
    else if (v.includes('seat')) violationCounts["Seat Belt"] += 1;
    else if (v.includes('triple') || v.includes('riding')) violationCounts["Triple Riding"] += 1;
    else if (v.includes('phone') || v.includes('mobile') || v.includes('distract')) violationCounts["Mobile Phone"] += 1;
    else if (v.includes('speed')) violationCounts["Speed"] += 1;
    else if (v.includes('red') || v.includes('light')) violationCounts["Red Light"] += 1;
    else if (v.includes('lane') || v.includes('wrong')) violationCounts["Wrong Lane"] += 1;
    else if (v.includes('stop') || v.includes('line')) violationCounts["Stop Line"] += 1;
    else if (v.includes('park')) violationCounts["Parking"] += 1;
    else if (v.includes('plate') || v.includes('ocr')) violationCounts["Number Plate"] += 1;
  });

  const totalViolations = Object.values(violationCounts).reduce((acc, curr) => acc + curr, 0);

  const vehicleCount = evidence.vehicles_count || 0;
  const frameCount = evidence.frame_count || 1;
  const duration = evidence.processing_time_sec || 0.0;

  // Calculate Violation Rate: total violations / vehicles detected
  const violationRate = vehicleCount > 0 ? ((totalViolations / vehicleCount) * 100).toFixed(1) : '0.0';

  const items = [
    { label: "Vehicles Detected", value: vehicleCount, icon: ShieldCheck, color: "text-purple-400" },
    { label: "Total Violations", value: totalViolations, icon: ShieldAlert, color: totalViolations > 0 ? "text-rose-400" : "text-slate-450" },
    { label: "Duration", value: `${duration} s`, icon: Clock, color: "text-sky-400" },
    { label: "Frames Processed", value: frameCount, icon: FileText, color: "text-indigo-400" }
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-5 select-none animate-fadeIn">
      <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center space-x-2">
        <BarChart2 className="w-4 h-4 text-purple-400" />
        <span>Detection Summary Metrics</span>
      </h4>

      <div className="grid grid-cols-2 gap-3">
        {items.map((item, idx) => {
          const Icon = item.icon;
          return (
            <div key={idx} className="bg-slate-950 border border-slate-850 p-3.5 rounded-xl flex items-center space-x-3">
              <div className={`p-2 rounded-lg bg-slate-900 flex-shrink-0 ${item.color}`}>
                <Icon className="w-4.5 h-4.5" />
              </div>
              <div className="min-w-0 flex-1">
                <span className="text-[9px] text-slate-500 uppercase font-extrabold tracking-wider block truncate">{item.label}</span>
                <span className="text-xs font-mono font-extrabold text-slate-200 mt-0.5 block">{item.value}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Violation Breakdown */}
      {totalViolations > 0 ? (
        <div className="bg-slate-950 border border-slate-850 p-4 rounded-xl space-y-3">
          <span className="text-[10px] text-slate-400 font-extrabold block uppercase tracking-wider border-b border-slate-850 pb-2">Violation Breakdown</span>
          
          <div className="space-y-2 text-xs font-semibold text-slate-350">
            {Object.entries(violationCounts).map(([type, count]) => {
              if (count === 0) return null;
              return (
                <div key={type} className="flex justify-between items-center bg-slate-900/40 px-3 py-1.5 rounded-lg border border-slate-850/50">
                  <span>{type}</span>
                  <span className="font-mono text-slate-200 font-extrabold">{count}</span>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between items-center pt-2.5 border-t border-slate-850 text-xs text-slate-400 font-bold">
            <span>Violation Rate</span>
            <span className="font-mono text-purple-400 font-extrabold">{violationRate}%</span>
          </div>
        </div>
      ) : (
        <div className="bg-slate-955/60 border border-slate-850 p-4 rounded-xl text-center text-xs text-slate-500 font-semibold leading-relaxed">
          No verified traffic violations detected.
        </div>
      )}
    </div>
  );
}
