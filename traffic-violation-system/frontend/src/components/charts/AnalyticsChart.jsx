import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';

export default function AnalyticsChart({ type, data }) {
  const COLORS = ['#aa3bff', '#6366f1', '#f43f5e', '#eab308', '#06b6d4'];

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-800 p-3 rounded-lg shadow-xl text-xs">
          <p className="font-semibold text-slate-200">{label}</p>
          {payload.map((p, idx) => (
            <p key={idx} style={{ color: p.color }}>
              {p.name}: {p.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  if (!data || data.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-slate-500 text-xs">
        No chart metrics data available
      </div>
    );
  }

  // 1. Line Chart for daily violation counts
  if (type === 'line') {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
          <Tooltip content={<CustomTooltip />} />
          <Line type="monotone" dataKey="count" name="Violations" stroke="#aa3bff" strokeWidth={2.5} activeDot={{ r: 6 }} />
        </LineChart>
      </ResponsiveContainer>
    );
  }

  // 2. Bar Chart for vehicle infraction categories
  if (type === 'bar') {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="type" stroke="#64748b" fontSize={10} tickLine={false} />
          <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="count" name="Count" fill="#6366f1" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    );
  }

  // 3. Pie Chart for distribution
  if (type === 'pie') {
    return (
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={80}
            paddingAngle={5}
            dataKey="count"
            nameKey="name"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend iconType="circle" wrapperStyle={{ fontSize: 10, color: '#94a3b8' }} />
        </PieChart>
      </ResponsiveContainer>
    );
  }

  return null;
}
