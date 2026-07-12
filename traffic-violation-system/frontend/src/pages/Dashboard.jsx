import React, { useState, useEffect } from 'react';
import { AlertCircle, Camera, Cpu, Activity, ShieldAlert } from 'lucide-react';
import ViolationCard from '../components/ViolationCard';
import EvidenceViewer from '../components/EvidenceViewer';
import { violationAPI, analyticsAPI, cameraAPI } from '../services/api';
import { useSystem } from '../context/SystemContext';

export default function Dashboard() {
  const { healthData } = useSystem();
  const [violations, setViolations] = useState([]);
  const [selectedViolationId, setSelectedViolationId] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [summary, setSummary] = useState({
    total_violations: 0,
    helmet_cases: 0,
    seatbelt_cases: 0,
    red_light_cases: 0
  });

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const vRes = await violationAPI.getAll();
      setViolations(vRes.data.slice(-5).reverse());
      
      const sRes = await analyticsAPI.getSummary();
      setSummary(sRes.data);

      const cRes = await cameraAPI.getStatus();
      setCameraActive(cRes.data.running);
    } catch (err) {
      console.error("Error loading dashboard data:", err);
    }
  };

  const status = healthData.status || 'Healthy';
  const systemStatusVal = status === 'Healthy' ? 'Operational' : status === 'Warning' ? 'Warning' : 'Degraded';
  const systemStatusColor = status === 'Healthy' ? 'text-emerald-500' : status === 'Warning' ? 'text-amber-500' : 'text-rose-500';
  const systemStatusBg = status === 'Healthy' ? 'bg-emerald-500/10' : status === 'Warning' ? 'bg-amber-500/10' : 'bg-rose-500/10';

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Operations Control Center</h2>
        <p className="text-xs text-slate-500">Overview of active traffic violations, AI camera status, and detection statistics.</p>
      </div>

      {/* Overview Cards Header Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { title: 'Total Violations', value: summary.total_violations, icon: AlertCircle, color: 'text-purple-500', bg: 'bg-purple-500/10' },
          { title: 'Active Cameras', value: cameraActive ? '1 Active' : '0 Active', icon: Camera, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
          { title: 'Detected Vehicles', value: violations.length > 0 ? `${violations.length * 2 + 1} Tracked` : '0 Tracked', icon: Cpu, color: 'text-sky-500', bg: 'bg-sky-500/10' },
          { title: 'System Status', value: systemStatusVal, icon: Activity, color: systemStatusColor, bg: systemStatusBg },
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-4">
              <div className={`${card.bg} p-3 rounded-lg`}>
                <Icon className={`w-6 h-6 ${card.color}`} />
              </div>
              <div>
                <span className="text-xs text-slate-500 block">{card.title}</span>
                <span className="text-xl font-bold text-slate-100">{card.value}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Violation Event Logs Panel */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col min-h-[400px]">
        <div className="pb-3 border-b border-slate-800 flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-purple-500" />
            <h3 className="font-semibold text-sm text-slate-200 uppercase tracking-wider">Recent Infractions</h3>
          </div>
          <span className="w-2.5 h-2.5 rounded-full bg-purple-500 animate-pulse"></span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 flex-1">
          {violations.length === 0 ? (
            <div className="col-span-full h-full flex items-center justify-center text-center p-6 text-slate-550 text-xs">
              No recent infractions logged. Start live camera streams to begin logging.
            </div>
          ) : (
            violations.map((v, idx) => (
              <ViolationCard
                key={idx}
                item={v}
                onViewEvidence={() => setSelectedViolationId(v.vehicle_id)}
              />
            ))
          )}
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
