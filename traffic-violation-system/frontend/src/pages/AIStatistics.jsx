import React, { useState, useEffect } from 'react';
import { statisticsAPI } from '../services/statisticsApi';
import StatisticsCards from '../components/statistics/StatisticsCards';
import AccuracyChart from '../components/statistics/AccuracyChart';
import ConfidenceChart from '../components/statistics/ConfidenceChart';
import DetectionChart from '../components/statistics/DetectionChart';
import PerformanceChart from '../components/statistics/PerformanceChart';

export default function AIStatistics() {
  const [overview, setOverview] = useState(null);
  const [daily, setDaily] = useState([]);
  const [weekly, setWeekly] = useState([]);
  const [monthly, setMonthly] = useState([]);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      const [resOver, resDaily, resWeekly, resMonthly, resPerf] = await Promise.all([
        statisticsAPI.getOverview(),
        statisticsAPI.getDaily(),
        statisticsAPI.getWeekly(),
        statisticsAPI.getMonthly(),
        statisticsAPI.getPerformance()
      ]);
      setOverview(resOver.data);
      setDaily(resDaily.data.daily || []);
      setWeekly(resWeekly.data.weekly || []);
      setMonthly(resMonthly.data.monthly || []);
      setPerformance(resPerf.data);
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
        <span>Loading AI Analytics Statistics...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">AI Statistics Dashboard</h2>
        <p className="text-xs text-slate-500">Real-time model accuracy metrics, latency measurements and detection counts.</p>
      </div>

      <StatisticsCards stats={overview} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left charts */}
        <div className="lg:col-span-2 space-y-6">
          <AccuracyChart data={daily} />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ConfidenceChart data={weekly} />
            <DetectionChart data={monthly} />
          </div>
        </div>

        {/* Right hardware */}
        <div>
          <PerformanceChart performance={performance} />
        </div>
      </div>
    </div>
  );
}
