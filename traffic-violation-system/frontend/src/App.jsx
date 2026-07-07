import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Violations from './pages/Violations';
import Evidence from './pages/Evidence';
import Analytics from './pages/Analytics';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [cameraActive, setCameraActive] = useState(false);

  // Tab switcher router mapping
  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'violations':
        return <Violations />;
      case 'evidence':
        return <Evidence />;
      case 'analytics':
        return <Analytics />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-purple-650 selection:text-white">
      {/* Navbar header */}
      <Navbar cameraActive={cameraActive} />

      {/* Main app panel */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar options */}
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

        {/* Dynamic routing page content */}
        <main className="flex-1 flex flex-col overflow-hidden bg-slate-950/20">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
