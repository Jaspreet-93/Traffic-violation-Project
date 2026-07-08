import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Lock, User } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'admin123') {
      localStorage.setItem('admin_logged_in', 'true');
      navigate('/dashboard');
    } else {
      setError('Invalid Administrator Credentials.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-955 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-md p-8 shadow-2xl relative overflow-hidden">
        {/* Glow accent */}
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -right-40 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl"></div>

        <div className="relative flex flex-col items-center mb-6">
          <div className="bg-purple-500/15 p-4 rounded-2xl border border-purple-500/30 mb-4">
            <Shield className="w-8 h-8 text-purple-400 animate-pulse" />
          </div>
          <h2 className="text-xl font-bold text-slate-100 uppercase tracking-wide">Aura Monitor Panel</h2>
          <span className="text-[10px] text-slate-500 mt-1 uppercase font-bold tracking-wider">Administrator Sign In</span>
        </div>

        <form onSubmit={handleLogin} className="space-y-4 relative">
          {error && (
            <div className="p-3 bg-rose-500/10 border border-rose-500/25 text-rose-450 text-xs font-bold rounded-xl text-center">
              {error}
            </div>
          )}

          <div>
            <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-550 absolute left-3 top-3" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="admin"
                required
                className="w-full bg-slate-955 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-200 placeholder-slate-700 outline-none transition-colors"
              />
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

          <button
            type="submit"
            className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow-lg shadow-purple-650/15 text-xs uppercase tracking-wider cursor-pointer"
          >
            Access Control Deck
          </button>
        </form>
      </div>
    </div>
  );
}
