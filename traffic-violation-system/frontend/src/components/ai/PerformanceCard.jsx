import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { Activity } from 'lucide-react';

export default function PerformanceCard({ performance }) {
  const [history, setHistory] = React.useState([]);

  React.useEffect(() => {
    if (performance) {
      setHistory((prev) => {
        const next = [...prev, {
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
          fps: performance.fps || 0.0,
          latency: performance.inference_time_ms || 0.0
        }];
        if (next.length > 15) next.shift();
        return next;
      });
    }
  }, [performance]);

  if (history.length === 0) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Activity className="w-4.5 h-4.5 text-purple-400 animate-pulse" />
        <span>Inference Latency & FPS Performance</span>
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[220px]">
        {/* Latency Chart */}
        <div className="flex flex-col h-full">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-2">Inference Latency (ms)</span>
          <ResponsiveContainer width="100%" height="90%">
            <AreaChart data={history} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
              <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" stroke="#64748b" fontSize={9} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={9} tickLine={false} />
              <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '10px' }} />
              <Area type="monotone" dataKey="latency" name="Latency" stroke="#aa3bff" fill="url(#latencyGlowCard)" strokeWidth={2} />
              <defs>
                <linearGradient id="latencyGlowCard" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#aa3bff" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#aa3bff" stopOpacity={0}/>
                </linearGradient>
              </defs>
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* FPS Chart */}
        <div className="flex flex-col h-full">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider mb-2">Throughput Rate (FPS)</span>
          <ResponsiveContainer width="100%" height="90%">
            <AreaChart data={history} margin={{ top: 5, right: 5, left: -25, bottom: 0 }}>
              <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="time" stroke="#64748b" fontSize={9} tickLine={false} />
              <YAxis stroke="#64748b" fontSize={9} tickLine={false} />
              <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '10px' }} />
              <Area type="monotone" dataKey="fps" name="Throughput" stroke="#6366f1" fill="url(#fpsGlowCard)" strokeWidth={2} />
              <defs>
                <linearGradient id="fpsGlowCard" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                </linearGradient>
              </defs>
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
