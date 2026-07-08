import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Lock, User, FileText, Landmark, Mail } from 'lucide-react';

export default function Login() {
  const [officerName, setOfficerName] = useState('');
  const [officerId, setOfficerId] = useState('');
  const [stationName, setStationName] = useState('');
  const [stationEmail, setStationEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (rememberMe) {
      localStorage.setItem('officer_name', officerName);
      localStorage.setItem('station_name', stationName);
    }
    // Simulate login and navigate to dashboard
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg p-8 shadow-2xl relative overflow-hidden">
        {/* Glow accent */}
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -right-40 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl"></div>

        <div className="relative flex flex-col items-center mb-6">
          <div className="bg-purple-500/15 p-4 rounded-2xl border border-purple-500/30 mb-4">
            <Shield className="w-8 h-8 text-purple-400 animate-pulse" />
          </div>
          <h2 className="text-2xl font-bold text-slate-100 uppercase tracking-wide">Aura Monitor Panel</h2>
          <span className="text-xs text-slate-500 mt-1">Smart Traffic Enforcement System Login</span>
        </div>

        <form onSubmit={handleLogin} className="space-y-4 relative">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Officer Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
                <input
                  type="text"
                  value={officerName}
                  onChange={(e) => setOfficerName(e.target.value)}
                  placeholder="John Doe"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Officer ID</label>
              <div className="relative">
                <FileText className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
                <input
                  type="text"
                  value={officerId}
                  onChange={(e) => setOfficerId(e.target.value)}
                  placeholder="TP-9821"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Station Name</label>
              <div className="relative">
                <Landmark className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
                <input
                  type="text"
                  value={stationName}
                  onChange={(e) => setStationName(e.target.value)}
                  placeholder="Central Traffic Station"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Official Station Email</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
                <input
                  type="email"
                  value={stationEmail}
                  onChange={(e) => setStationEmail(e.target.value)}
                  placeholder="station@traffic.gov"
                  required
                  className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
                />
              </div>
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
              />
            </div>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="rememberMe"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="rounded bg-slate-955 border-slate-850 text-purple-650 focus:ring-purple-500/40 w-4 h-4 mr-2 cursor-pointer"
            />
            <label htmlFor="rememberMe" className="text-xs text-slate-450 cursor-pointer select-none">
              Remember credentials for this terminal
            </label>
          </div>

          <button
            type="submit"
            className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow-lg shadow-purple-650/15 text-xs uppercase tracking-wider"
          >
            Access Control Deck
          </button>
        </form>
      </div>
    </div>
  );
}
