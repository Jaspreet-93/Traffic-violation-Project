import React from 'react';
import { Globe } from 'lucide-react';

export default function LanguageSettings({ settings, onChange }) {
  const langs = [
    { label: 'English', code: 'en' },
    { label: 'Hindi', code: 'hi' },
    { label: 'Spanish', code: 'es' }
  ];

  const current = settings.language || 'en';

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4 flex flex-col justify-between">
      <h4 className="text-xs font-bold text-slate-550 uppercase tracking-wider flex items-center space-x-1.5">
        <Globe className="w-4 h-4 text-purple-400" />
        <span>System Language</span>
      </h4>
      <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
        {langs.map((l) => (
          <button
            key={l.code}
            onClick={() => onChange('language', l.code)}
            className={`flex-1 py-1.5 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
              current === l.code ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            {l.label}
          </button>
        ))}
      </div>
    </div>
  );
}
