import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './components/common/Navbar';
import Sidebar from './components/common/Sidebar';
import AppRoutes from './routes/AppRoutes';
import { cameraAPI } from './services/api';

export default function App() {
  const location = useLocation();
  const isLoginPage = location.pathname === '/login';
  const [sidebarOpen, setSidebarOpen] = useState(false);

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

  // Close sidebar on route change on mobile
  useEffect(() => {
    setSidebarOpen(false);
  }, [location]);

  return (
    <div className="min-h-screen flex flex-col bg-slate-955 text-slate-100 selection:bg-purple-650 selection:text-white">
      {/* Show navigation controls only outside Login panel */}
      {!isLoginPage && (
        <Navbar 
          onToggleSidebar={() => setSidebarOpen(!sidebarOpen)} 
        />
      )}

      <div className="flex-1 flex overflow-hidden relative">
        {!isLoginPage && (
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        )}

        {/* Mobile Backdrop overlay */}
        {!isLoginPage && sidebarOpen && (
          <div 
            onClick={() => setSidebarOpen(false)} 
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-30 lg:hidden cursor-pointer"
          ></div>
        )}

        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950/20 w-full">
          <AppRoutes />
        </main>
      </div>
    </div>
  );
}
