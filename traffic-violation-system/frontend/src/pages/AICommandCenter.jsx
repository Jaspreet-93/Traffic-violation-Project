import React, { useState, useEffect } from 'react';
import { aiCommandCenterAPI } from '../services/aiCommandCenterApi';
import AIOverviewCard from '../components/ai/AIOverviewCard';
import ModelHealthCard from '../components/ai/ModelHealthCard';
import SystemHealthCard from '../components/ai/SystemHealthCard';
import HardwareCard from '../components/ai/HardwareCard';
import ConfidenceCard from '../components/ai/ConfidenceCard';
import CameraStatusCard from '../components/ai/CameraStatusCard';
import PerformanceCard from '../components/ai/PerformanceCard';

export default function AICommandCenter() {
  const [overview, setOverview] = useState(null);
  const [models, setModels] = useState([]);
  const [systemHealth, setSystemHealth] = useState(null);
  const [hardware, setHardware] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchCenterData = async () => {
    try {
      const [
        resOverview,
        resSystem,
        resModels,
        resHardware,
        resConfidence,
        resPerformance
      ] = await Promise.all([
        aiCommandCenterAPI.getOverview(),
        aiCommandCenterAPI.getSystemHealth(),
        aiCommandCenterAPI.getModelHealth(),
        aiCommandCenterAPI.getHardware(),
        aiCommandCenterAPI.getConfidence(),
        aiCommandCenterAPI.getPerformance()
      ]);

      setOverview(resOverview.data);
      setSystemHealth(resSystem.data);
      setModels(resModels.data.models || []);
      setHardware(resHardware.data);
      setConfidence(resConfidence.data);
      setPerformance(resPerformance.data);
    } catch (err) {
      console.error("Error gathering Enterprise Stage 1 Command Center statistics:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCenterData();
    const interval = setInterval(fetchCenterData, 3000); // 3s polling refresh
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center space-y-3 p-12 text-slate-500 text-xs">
        <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading Enterprise AI Command Center...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Command Center</h2>
        <p className="text-xs text-slate-500">Real-time surveillance monitoring and hardware diagnostic dashboard.</p>
      </div>

      {/* 1. Overview aggregates */}
      <AIOverviewCard overview={overview} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Columns (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Models health stats */}
          <ModelHealthCard modelData={models} />
          
          {/* Performance area graph */}
          <PerformanceCard performance={performance} />
        </div>

        {/* Right Columns (1 col) */}
        <div className="space-y-6">
          {/* Gauges stats */}
          <SystemHealthCard health={systemHealth} />

          {/* Core Hardware specs */}
          <HardwareCard hardware={hardware} />

          {/* Camera status active counts */}
          <CameraStatusCard overview={overview} />

          {/* Live confidence scores */}
          <ConfidenceCard confidence={confidence} />
        </div>
      </div>
    </div>
  );
}
