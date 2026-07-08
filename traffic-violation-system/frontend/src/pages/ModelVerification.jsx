import React, { useState, useEffect } from 'react';
import { modelVerificationAPI } from '../services/modelVerificationApi';
import ModelOverview from '../components/model/ModelOverview';
import ModelHealthCard from '../components/model/ModelHealthCard';
import MetricsCard from '../components/model/MetricsCard';
import DatasetSummary from '../components/model/DatasetSummary';
import PerformanceCharts from '../components/model/PerformanceCharts';
import BenchmarkTable from '../components/model/BenchmarkTable';
import RecommendationPanel from '../components/model/RecommendationPanel';
import VerificationStatus from '../components/model/VerificationStatus';

export default function ModelVerification() {
  const [overview, setOverview] = useState(null);
  const [health, setHealth] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [benchmarks, setBenchmarks] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [verification, setVerification] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [
        resOver,
        resHealth,
        resMetrics,
        resData,
        resPerf,
        resBench,
        resRecs,
        resVerif
      ] = await Promise.all([
        modelVerificationAPI.getOverview(),
        modelVerificationAPI.getHealth(),
        modelVerificationAPI.getMetrics(),
        modelVerificationAPI.getDataset(),
        modelVerificationAPI.getPerformance(),
        modelVerificationAPI.getBenchmark(),
        modelVerificationAPI.getRecommendations(),
        modelVerificationAPI.getVerification()
      ]);
      setOverview(resOver.data);
      setHealth(resHealth.data);
      setMetrics(resMetrics.data);
      setDataset(resData.data);
      setPerformance(resPerf.data);
      setBenchmarks(resBench.data.benchmarks || []);
      setRecommendations(resRecs.data.recommendations || []);
      setVerification(resVerif.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-550 text-xs">
        <span>Loading Verification Console...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Model Verification Center</h2>
        <p className="text-xs text-slate-500">Run diagnostics validation check, view epoch metrics and latency benchmarks.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          <ModelOverview overview={overview} />

          <PerformanceCharts performance={performance} />

          <BenchmarkTable benchmarks={benchmarks} />

          <MetricsCard metrics={metrics} />
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          <VerificationStatus verification={verification} />

          <ModelHealthCard health={health} />

          <DatasetSummary dataset={dataset} />

          <RecommendationPanel recommendations={recommendations} />
        </div>
      </div>
    </div>
  );
}
