import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';
import AppRoutes from './routes/AppRoutes';
import { cameraAPI } from './services/api';

export default function App() {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const [cameraActive, setCameraActive] = useState(false);

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const { settingsAPI } = await import('./services/settingsApi');
        const res = await settingsAPI.getSettings();
        const theme = res.data.theme || 'dark';
        const lang = res.data.language || 'en';
        
        localStorage.setItem('system_theme', theme);
        localStorage.setItem('system_language', lang);

        if (theme === 'light') {
          document.documentElement.classList.add('light');
        } else {
          document.documentElement.classList.remove('light');
        }
      } catch (err) {
        console.error("Failed to load settings:", err);
      }
    };
    loadSettings();
  }, []);

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
          <AppRoutes />
        </main>
      </div>
    </div>
  );
}
