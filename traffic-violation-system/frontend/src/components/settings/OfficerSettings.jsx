import React, { useState, useEffect } from 'react';
import { User, Shield } from 'lucide-react';

export default function OfficerSettings() {
  const [officerName, setOfficerName] = useState('');
  const [officerId, setOfficerId] = useState('');

  useEffect(() => {
    setOfficerName(localStorage.getItem('officer_name') || '');
    setOfficerId(localStorage.getItem('officer_id') || '');
  }, []);

  const handleSave = () => {
    localStorage.setItem('officer_name', officerName);
    localStorage.setItem('officer_id', officerId);
    alert('Officer credentials updated successfully!');
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col space-y-4">
      <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
        <Shield className="w-4.5 h-4.5 text-purple-400" />
        <span>Officer Identity Panel</span>
      </h3>

      <div className="space-y-4">
        <div>
          <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Officer Name</label>
          <input
            type="text"
            value={officerName}
            onChange={(e) => setOfficerName(e.target.value)}
            placeholder="John Doe"
            className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
          />
        </div>

        <div>
          <label className="text-xs font-bold text-slate-450 uppercase block mb-1">Officer Badge ID</label>
          <input
            type="text"
            value={officerId}
            onChange={(e) => setOfficerId(e.target.value)}
            placeholder="TP-9821"
            className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none transition-colors"
          />
        </div>

        <button
          onClick={handleSave}
          className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs uppercase tracking-wider cursor-pointer"
        >
          Save Officer Profile
        </button>
      </div>
    </div>
  );
}
