import React, { useState } from 'react';
import EmailSettings from '../components/settings/EmailSettings';
import SMTPStatusCard from '../components/settings/SMTPStatusCard';

export default function Settings() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleSettingsUpdate = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">System Settings</h2>
        <p className="text-xs text-slate-500">Configure SMTP servers, official station destination emails, and toggle automated alerts.</p>
      </div>

      {/* Settings Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <EmailSettings onStatusChange={handleSettingsUpdate} />
        </div>
        <div>
          <SMTPStatusCard refreshTrigger={refreshKey} />
        </div>
      </div>
    </div>
  );
}
