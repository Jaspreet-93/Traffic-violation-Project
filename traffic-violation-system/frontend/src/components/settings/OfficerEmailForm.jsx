import React, { useState, useEffect } from 'react';
import { Mail, Check, X } from 'lucide-react';

export default function OfficerEmailForm({ editItem, onSave, onCancel }) {
  const [emailAddress, setEmailAddress] = useState('');
  const [active, setActive] = useState(true);
  const [primary, setPrimary] = useState(false);

  useEffect(() => {
    if (editItem) {
      setEmailAddress(editItem.email_address);
      setActive(editItem.active);
      setPrimary(editItem.primary);
    } else {
      setEmailAddress('');
      setActive(true);
      setPrimary(false);
    }
  }, [editItem]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!emailAddress.trim()) return;
    onSave({
      email_address: emailAddress.trim(),
      active,
      primary
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-950/20 border border-slate-850 p-4 rounded-xl space-y-4 shadow-inner">
      <div className="flex justify-between items-center text-xs">
        <h4 className="font-bold text-slate-200">
          {editItem ? 'Edit Officer Recipient Email' : 'Add New Officer Recipient Email'}
        </h4>
        {editItem && (
          <button
            type="button"
            onClick={onCancel}
            className="text-slate-500 hover:text-slate-350 cursor-pointer flex items-center space-x-1"
          >
            <X className="w-3.5 h-3.5" />
            <span>Cancel Edit</span>
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Email Address</label>
          <div className="relative">
            <Mail className="w-4 h-4 text-slate-600 absolute left-3 top-2.5" />
            <input
              type="email"
              value={emailAddress}
              onChange={(e) => setEmailAddress(e.target.value)}
              placeholder="officer@traffic.gov"
              required
              className="w-full bg-slate-950 border border-slate-850 focus:border-purple-500/80 rounded-xl py-2 pl-10 pr-4 text-xs text-slate-250 placeholder-slate-700 outline-none transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center space-x-6 md:pt-4">
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="activeFlag"
              checked={active}
              onChange={(e) => setActive(e.target.checked)}
              className="rounded bg-slate-950 border-slate-850 text-purple-650 focus:ring-purple-500/40 w-4 h-4 cursor-pointer"
            />
            <label htmlFor="activeFlag" className="text-xs text-slate-400 font-bold select-none cursor-pointer">
              Active Alerts
            </label>
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="primaryFlag"
              checked={primary}
              onChange={(e) => setPrimary(e.target.checked)}
              className="rounded bg-slate-950 border-slate-850 text-purple-650 focus:ring-purple-500/40 w-4 h-4 cursor-pointer"
            />
            <label htmlFor="primaryFlag" className="text-xs text-slate-400 font-bold select-none cursor-pointer">
              Primary Recipient
            </label>
          </div>
        </div>
      </div>

      <button
        type="submit"
        className="w-full bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs flex items-center justify-center space-x-1.5 cursor-pointer"
      >
        <Check className="w-4 h-4" />
        <span>{editItem ? 'Update Recipient' : 'Register Recipient'}</span>
      </button>
    </form>
  );
}
