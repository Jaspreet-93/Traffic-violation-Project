import React, { useState, useEffect } from 'react';
import { confidenceAPI } from '../services/confidenceApi';
import ConfidenceCard from '../components/confidence/ConfidenceCard';
import TrustScoreCard from '../components/confidence/TrustScoreCard';
import ConfidenceChart from '../components/confidence/ConfidenceChart';
import ModelComparison from '../components/confidence/ModelComparison';
import DetectionTimeline from '../components/confidence/DetectionTimeline';
import ConfidenceHistory from '../components/confidence/ConfidenceHistory';
import OverallScore from '../components/confidence/OverallScore';
import RuntimeStatus from '../components/confidence/RuntimeStatus';

export default function ConfidenceDashboard() {
  const [live, setLive] = useState(null);
  const [history, setHistory] = useState([]);
  const [models, setModels] = useState([]);
  const [trust, setTrust] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const [
        resLive,
        resHistory,
        resModels,
        resTrust,
        resStats
      ] = await Promise.all([
        confidenceAPI.getLiveConfidence(),
        confidenceAPI.getHistory(),
        confidenceAPI.getModels(),
        confidenceAPI.getTrustScore(),
        confidenceAPI.getStatistics()
      ]);

      setLive(resLive.data);
      setHistory(resHistory.data.history || []);
      setModels(resModels.data.models || []);
      setTrust(resTrust.data);
      setStats(resStats.data);
    } catch (err) {
      console.error("Error fetching confidence dashboard statistics:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 3000); // 3s polling refresh
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center space-y-3 p-12 text-slate-550 text-xs">
        <span className="w-6 h-6 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading AI Confidence Dashboard...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Confidence & Trust</h2>
        <p className="text-xs text-slate-500">Real-time indicators, precision averages, and overall classifier trust ratings.</p>
      </div>

      {/* Dials & Gauges Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <TrustScoreCard trust={trust} />
        <ConfidenceCard confidence={live} />
        
        <div className="space-y-6">
          <OverallScore trust={trust} />
          <RuntimeStatus stats={stats} />
        </div>
      </div>

      {/* Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Trend Area Chart */}
          <ConfidenceChart trend={stats?.confidence_trend} avg={stats?.average_confidence} />
          
          {/* Latency Timeline Chart */}
          <DetectionTimeline timeline={stats?.processing_time_trend} />
        </div>
        
        <div>
          {/* Model Comparison Bar Chart */}
          <ModelComparison data={stats?.model_comparison} />
        </div>
      </div>

      {/* History table */}
      <ConfidenceHistory historyList={history} />
    </div>
  );
}
