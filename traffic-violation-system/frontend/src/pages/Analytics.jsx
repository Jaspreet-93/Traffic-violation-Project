import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, AlertTriangle, ShieldCheck } from 'lucide-react';
import { analyticsAPI } from '../services/api';
import AnalyticsChart from '../components/AnalyticsChart';

export default function Analytics() {
  const [summary, setSummary] = useState(null);
  const [dailyData, setDailyData] = useState([]);
  const [typeData, setTypeData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      
      const sRes = await analyticsAPI.getSummary();
      setSummary(sRes.data);
      
      const dRes = await analyticsAPI.getDaily();
      setDailyData(dRes.data);
      
      const tRes = await analyticsAPI.getTypes();
      setTypeData(tRes.data);
    } catch (err) {
      console.error("Error loading analytics data:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <span className="w-8 h-8 rounded-full border-4 border-purple-500 border-t-transparent animate-spin"></span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Analytics Insights</h2>
        <p className="text-xs text-slate-500">Track traffic infraction trends, daily reports, and violation distributions.</p>
      </div>

      {/* Summary grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Violations', value: summary?.total_violations || 0, icon: AlertTriangle, color: 'text-purple-400', bg: 'bg-purple-500/10' },
          { label: 'Helmet Cases', value: summary?.helmet_cases || 0, icon: ShieldCheck, color: 'text-amber-400', bg: 'bg-amber-500/10' },
          { label: 'Seatbelt Cases', value: summary?.seatbelt_cases || 0, icon: TrendingUp, color: 'text-sky-400', bg: 'bg-sky-500/10' },
          { label: 'Red Light Cases', value: summary?.red_light_cases || 0, icon: BarChart3, color: 'text-rose-400', bg: 'bg-rose-500/10' },
        ].map((card, idx) => {
          const Icon = card.icon;
          return (
            <div key={idx} className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex items-center space-x-3">
              <div className={`${card.bg} p-2.5 rounded-lg`}>
                <Icon className={`w-5 h-5 ${card.color}`} />
              </div>
              <div>
                <span className="text-[10px] text-slate-550 block uppercase font-bold tracking-wider">{card.label}</span>
                <span className="text-xl font-bold text-slate-200">{card.value}</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Daily trend area chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col h-[350px]">
          <h3 className="font-semibold text-sm text-slate-350 mb-4 flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-purple-500" />
            <span>Daily Infraction Trends</span>
          </h3>
          <div className="flex-1 min-h-0">
            <AnalyticsChart type="area" data={dailyData} />
          </div>
        </div>

        {/* Category distribution bar chart */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 flex flex-col h-[350px]">
          <h3 className="font-semibold text-sm text-slate-350 mb-4 flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-indigo-500" />
            <span>Distribution by Infraction Types</span>
          </h3>
          <div className="flex-1 min-h-0">
            <AnalyticsChart type="bar" data={typeData} />
          </div>
        </div>
      </div>
    </div>
  );
}
