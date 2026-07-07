import React, { useState, useEffect } from 'react';
import { ShieldCheck, AlertCircle, Camera, Award } from 'lucide-react';
import LiveFeed from '../components/LiveFeed';
import ViolationCard from '../components/ViolationCard';
import EvidenceViewer from '../components/EvidenceViewer';
import { violationAPI, analyticsAPI } from '../services/api';

export default function Dashboard() {
  const [cameraActive, setCameraActive] = useState(false);
  const [violations, setViolations] = useState([]);
  const [selectedViolationId, setSelectedViolationId] = useState(null);
  const [summary, setSummary] = useState({
    total_violations: 0,
    helmet_cases: 0,
    seatbelt_cases: 0,
    red_light_cases: 0
  });

  useEffect(() => {
    fetchData();
    // Poll updates every 3 seconds for real-time reactivity
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const vRes = await violationAPI.getAll();
      // Only keep latest 5 violations
      setViolations(vRes.data.slice(-5).reverse());
      
      const sRes = await analyticsAPI.getSummary();
      setSummary(sRes.data);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Overview Cards Header Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Total Violations', value: summary.total_violations, icon: AlertCircle, color: 'text-purple-500', bg: 'bg-purple-500/10' },
          { title: 'Helmet Violations', value: summary.helmet_cases, icon: ShieldCheck, color: 'text-amber-500', bg: 'bg-amber-500/10' },
          { title: 'Seatbelt Violations', value: summary.seatbelt_cases, icon: Award, color: 'text-sky-500', bg: 'bg-sky-500/10' },
          { title: 'Red Light Violations', value: summary.red_light_cases, icon: Camera, color: 'text-rose-500', bg: 'bg-rose-500/10' },
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-4">
              <div className={`${card.bg} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
              <div>
                <span className="text-xs text-slate-500 block">{card.title}</span>
                <span className="text-2xl font-bold text-slate-100">{card.value}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main Grid: Stream & Pipeline vs Recent Violations */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stream & switches (left cols) */}
        <div className="lg:col-span-2">
          <LiveFeed onStreamStateChange={setCameraActive} />
        </div>

        {/* Real-time violations list (right col) */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col h-[610px]">
          <div className="pb-3 border-b border-slate-800 flex items-center justify-between mb-4">
            <h3 className="font-semibold text-sm text-slate-200 uppercase tracking-wider">Live Violation Logs</h3>
            <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-3 pr-1">
            {violations.length === 0 ? (
              <div className="h-full flex items-center justify-center text-center p-6 text-slate-500 text-xs">
                Waiting for violations... Start the stream and activate AI detection modules.
              </div>
            ) : (
              violations.map((v, idx) => (
                <ViolationCard
                  key={idx}
                  item={v}
                  onViewEvidence={() => setSelectedViolationId(v.vehicle_id)} // maps vehicle_id to search evidence
                />
              ))
            )}
          </div>
        </div>
      </div>

      {/* Modal Evidence Reviewer popup */}
      {selectedViolationId && (
        <EvidenceViewer
          violationId={selectedViolationId}
          onClose={() => setSelectedViolationId(null)}
        />
      )}
    </div>
  );
}
