import React from 'react';
import { Sun, Moon } from 'lucide-react';

export default function ThemeSettings({ settings, onChange }) {
  const current = settings.theme || 'dark';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4 flex flex-col justify-between">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider">Interface Skin</h4>
      <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
        <button
          onClick={() => onChange('theme', 'dark')}
          className={`flex-1 py-1.5 rounded text-[10px] font-bold uppercase transition-all flex items-center justify-center space-x-1 cursor-pointer ${
            current === 'dark' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
          }`}
        >
          <Moon className="w-3.5 h-3.5" />
          <span>Dark Mode</span>
        </button>
        <button
          onClick={() => onChange('theme', 'light')}
          className={`flex-1 py-1.5 rounded text-[10px] font-bold uppercase transition-all flex items-center justify-center space-x-1 cursor-pointer ${
            current === 'light' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
          }`}
        >
          <Sun className="w-3.5 h-3.5" />
          <span>Light Mode</span>
        </button>
      </div>
    </div>
  );
}
