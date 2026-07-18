import React, { useState, useEffect } from 'react';
import { settingsAPI } from '../services/settingsApi';
import SMTPSettings from '../components/settings/SMTPSettings';
import AISettings from '../components/settings/AISettings';
import CameraSettings from '../components/settings/CameraSettings';
import StorageSettings from '../components/settings/StorageSettings';
import ThemeSettings from '../components/settings/ThemeSettings';
import LanguageSettings from '../components/settings/LanguageSettings';
import OfficerEmailManagement from '../components/settings/OfficerEmailManagement';
import EmailSettings from '../components/settings/EmailSettings';
import { Save, Mail, Server, Cpu, Video, Settings as SettingsIcon, ShieldCheck } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('officer'); // 'officer' | 'smtp' | 'ai' | 'stream' | 'appearance'

  const loadData = async () => {
    try {
      const res = await settingsAPI.getSettings();
      setSettings(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleChange = (key, val) => {
    setSettings(prev => ({
      ...prev,
      [key]: val
    }));

    if (key === 'theme') {
      localStorage.setItem('system_theme', val);
      if (val === 'light') {
        document.documentElement.classList.add('light');
      } else {
        document.documentElement.classList.remove('light');
      }
    }

    if (key === 'language') {
      localStorage.setItem('system_language', val);
      window.dispatchEvent(new Event('local-language-change'));
    }
  };

  const handleSave = async () => {
    try {
      const res = await settingsAPI.updateSettings(settings);
      setSettings(res.data);
      
      const theme = res.data.theme || 'dark';
      const lang = res.data.language || 'en';
      
      localStorage.setItem('system_theme', theme);
      localStorage.setItem('system_language', lang);

      if (theme === 'light') {
        document.documentElement.classList.add('light');
      } else {
        document.documentElement.classList.remove('light');
      }
      
      alert("System configurations successfully saved!");
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Failed to modify settings.");
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-550 text-xs">
        <span>Loading System Control Deck...</span>
      </div>
    );
  }

  const tabs = [
    { id: 'officer', label: 'Officer Recipients', icon: Mail },
    { id: 'smtp', label: 'SMTP Server', icon: Server },
    { id: 'ai', label: 'Inference Thresholds', icon: Cpu },
    { id: 'stream', label: 'Stream & Storage', icon: Video },
    { id: 'appearance', label: 'Appearance & Translation', icon: SettingsIcon },
  ];

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header Deck */}
      <div className="flex justify-between items-center border-b border-slate-850 pb-5">
        <div>
          <h2 className="text-2xl font-bold text-slate-100 flex items-center space-x-2">
            <SettingsIcon className="w-6 h-6 text-purple-400" />
            <span>System Control Deck</span>
          </h2>
          <p className="text-xs text-slate-500">Configure parameters, dispatch nodes, SMTP settings and localized flags.</p>
        </div>
        <button
          onClick={handleSave}
          className="px-4 py-2 bg-purple-650 hover:bg-purple-750 text-white font-semibold rounded-lg text-xs flex items-center space-x-1.5 transition-all shadow-md shadow-purple-650/15 cursor-pointer"
        >
          <Save className="w-4 h-4" />
          <span>Save Changes</span>
        </button>
      </div>

      {/* Quick Status Stats Widgets */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow space-y-1">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Active SMTP Host</span>
          <span className="text-xs font-mono text-slate-200 block">{settings?.smtp_user || 'Not Configured'}</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow space-y-1">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">AI Confidence limit</span>
          <span className="text-xs font-mono text-purple-450 block font-bold">{settings?.yolo_confidence_threshold || '0.75'}</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow space-y-1">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Storage Retention</span>
          <span className="text-xs font-mono text-slate-200 block">{settings?.retention_days || '30'} Days</span>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow space-y-1">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Interface language</span>
          <span className="text-xs font-mono text-slate-200 block uppercase font-bold">{settings?.language || 'en'}</span>
        </div>
      </div>

      {/* Main Settings Navigation Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Side Tab Navigation */}
        <div className="lg:col-span-1 flex flex-col space-y-1.5">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-xs font-semibold transition-all border text-left cursor-pointer ${
                  activeTab === tab.id
                    ? 'bg-purple-650 border-purple-500/30 text-white shadow-lg shadow-purple-650/10'
                    : 'bg-slate-900/60 border-slate-850 text-slate-450 hover:bg-slate-900 hover:text-slate-200'
                }`}
              >
                <Icon className="w-4 h-4 flex-shrink-0" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Right Side Content Panel */}
        <div className="lg:col-span-3 space-y-6">
          {activeTab === 'officer' && (
            <div className="grid grid-cols-1 gap-6">
              <OfficerEmailManagement />
            </div>
          )}

          {activeTab === 'smtp' && (
            <div className="grid grid-cols-1 gap-6">
              <SMTPSettings settings={settings} onChange={handleChange} />
              <EmailSettings onStatusChange={loadData} />
            </div>
          )}

          {activeTab === 'ai' && (
            <div className="grid grid-cols-1 gap-6">
              <AISettings settings={settings} onChange={handleChange} />
            </div>
          )}

          {activeTab === 'stream' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <CameraSettings settings={settings} onChange={handleChange} />
              <StorageSettings settings={settings} onChange={handleChange} />
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <ThemeSettings settings={settings} onChange={handleChange} />
              <LanguageSettings settings={settings} onChange={handleChange} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
