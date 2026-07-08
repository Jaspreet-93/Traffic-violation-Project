import React, { useState, useEffect } from 'react';
import { settingsAPI } from '../services/settingsApi';
import SMTPSettings from '../components/settings/SMTPSettings';
import AISettings from '../components/settings/AISettings';
import CameraSettings from '../components/settings/CameraSettings';
import StorageSettings from '../components/settings/StorageSettings';
import ThemeSettings from '../components/settings/ThemeSettings';
import LanguageSettings from '../components/settings/LanguageSettings';
import OfficerEmailManagement from '../components/settings/OfficerEmailManagement';
import { Save } from 'lucide-react';

export default function Settings() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);

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
      // Reload page to re-translate sidebar links instantly
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Failed to modify settings.");
    }
  };

  if (loading) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center text-slate-550 text-xs">
        <span>Loading System Settings...</span>
      </div>
    );
  }

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">System Settings</h2>
          <p className="text-xs text-slate-500">Configure thresholds, SMTP parameters, languages and timezone properties.</p>
        </div>
        <button
          onClick={handleSave}
          className="px-4 py-2 bg-purple-650 hover:bg-purple-750 text-white font-semibold rounded-lg text-xs flex items-center space-x-1.5 transition-all shadow-md shadow-purple-650/15 cursor-pointer"
        >
          <Save className="w-4 h-4" />
          <span>Save Changes</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <OfficerEmailManagement />
        <SMTPSettings settings={settings} onChange={handleChange} />
        <AISettings settings={settings} onChange={handleChange} />
        <CameraSettings settings={settings} onChange={handleChange} />
        <StorageSettings settings={settings} onChange={handleChange} />
        <ThemeSettings settings={settings} onChange={handleChange} />
        <LanguageSettings settings={settings} onChange={handleChange} />
      </div>
    </div>
  );
}
