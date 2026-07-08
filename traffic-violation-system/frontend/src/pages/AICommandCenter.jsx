import React, { useState, useEffect } from 'react';
import { aiAPI } from '../services/aiApi';
import AIOverview from '../components/ai/AIOverview';
import SystemHealthCard from '../components/ai/SystemHealthCard';
import PipelineMonitor from '../components/ai/PipelineMonitor';
import ModelHealthTable from '../components/ai/ModelHealthTable';
import ConfidenceMonitor from '../components/ai/ConfidenceMonitor';
import DatasetHealth from '../components/ai/DatasetHealth';
import PerformanceChart from '../components/ai/PerformanceChart';
import HardwareMonitor from '../components/ai/HardwareMonitor';
import DiagnosticsPanel from '../components/ai/DiagnosticsPanel';
import RecommendationPanel from '../components/ai/RecommendationPanel';
import TrainingMetrics from '../components/ai/TrainingMetrics';
import ReportGenerator from '../components/ai/ReportGenerator';
import BenchmarkCard from '../components/ai/BenchmarkCard';

export default function AICommandCenter() {
  const [overview, setOverview] = useState(null);
  const [models, setModels] = useState([]);
  const [training, setTraining] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [confidence, setConfidence] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [benchmark, setBenchmark] = useState([]);
  const [hardware, setHardware] = useState(null);
  const [diagnostics, setDiagnostics] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchAllData = async () => {
    try {
      const [
        resOverview,
        resModels,
        resDatasets,
        resConfidence,
        resPerformance,
        resBenchmark,
        resHardware,
        resDiagnostics,
        resRecs
      ] = await Promise.all([
        aiAPI.getOverview(),
        aiAPI.getModels(),
        aiAPI.getDatasets(),
        aiAPI.getConfidence(),
        aiAPI.getPerformance(),
        aiAPI.getBenchmark(),
        aiAPI.getSystemHealth(),
        aiAPI.getDiagnostics(),
        aiAPI.getRecommendations()
      ]);

      setOverview(resOverview.data);
      setModels(resModels.data);
      setDatasets(resDatasets.data);
      setConfidence(resConfidence.data);
      setPerformance(resPerformance.data);
      setBenchmark(resBenchmark.data);
      setHardware(resHardware.data);
      setDiagnostics(resDiagnostics.data.issues || []);
      setRecommendations(resRecs.data.recommendations || []);

      // Lazily query training metrics as it might fail back to 404 cleanly
      try {
        const resTraining = await aiAPI.getTrainingMetrics();
        setTraining(resTraining.data);
      } catch {
        setTraining(null);
      }

    } catch (err) {
      console.error("Failed to compile AI Command Center data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAllData();
    const interval = setInterval(fetchAllData, 4000); // refresh stats every 4s
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center space-y-3 p-12 text-slate-500 text-xs">
        <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading AI Command Center modules...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Command Center</h2>
        <p className="text-xs text-slate-500">Monitor health validator parameters, benchmark inference throughput, and track model precision curves.</p>
      </div>

      {/* 1. System Overview Metrics row */}
      <AIOverview overview={overview} />

      {/* 2. Pipeline Stages workflow */}
      <PipelineMonitor models={models} overview={overview} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Models Health Table */}
          <ModelHealthTable models={models} />

          {/* Dataset volume splits */}
          <DatasetHealth datasets={datasets} />

          {/* Performance Area Charts */}
          <PerformanceChart performance={performance} />

          {/* Training curves validation */}
          <TrainingMetrics metrics={training} />
        </div>

        {/* Right Side (1 col) */}
        <div className="space-y-6">
          {/* Resource gauges */}
          <SystemHealthCard overview={overview} />

          {/* Hardware status specifications */}
          <HardwareMonitor hardware={hardware} />

          {/* Live confidence dials */}
          <ConfidenceMonitor confidence={confidence} />

          {/* Throughput max charts */}
          <BenchmarkCard benchmark={benchmark} />

          {/* Diagnostics Panel */}
          <DiagnosticsPanel diagnostics={diagnostics} />

          {/* Actionable recommendations list */}
          <RecommendationPanel recommendations={recommendations} />

          {/* Export Report Card */}
          <ReportGenerator />
        </div>
      </div>
    </div>
  );
}
