import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import LiveMonitoring from './pages/LiveMonitoring';
import Violations from './pages/Violations';
import Evidence from './pages/Evidence';
import Analytics from './pages/Analytics';
import { cameraAPI } from './services/api';

export default function App() {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const [cameraActive, setCameraActive] = useState(false);

  // Poll status occasionally to keep Navbar sync active
  useEffect(() => {
    if (!isLoginPage) {
      const fetchCamStatus = async () => {
        try {
          const res = await cameraAPI.getStatus();
          setCameraActive(res.data.running);
        } catch {}
      };
      fetchCamStatus();
      const interval = setInterval(fetchCamStatus, 5000);
      return () => clearInterval(interval);
    }
  }, [isLoginPage]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-purple-650 selection:text-white">
      {/* Show navigation controls only outside Login panel */}
      {!isLoginPage && <Navbar cameraActive={cameraActive} />}

      <div className="flex-1 flex overflow-hidden">
        {!isLoginPage && <Sidebar />}

        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950/20">
          <Routes>
            <Route path="/" element={<Navigate to="/login" replace />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/live-monitoring" element={<LiveMonitoring />} />
            <Route path="/violations" element={<Violations />} />
            <Route path="/evidence" element={<Evidence />} />
            <Route path="/analytics" element={<Analytics />} />
            {/* Fallback */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}
