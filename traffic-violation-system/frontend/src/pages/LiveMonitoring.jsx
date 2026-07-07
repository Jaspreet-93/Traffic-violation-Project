import React, { useState } from 'react';
import LiveFeed from '../components/LiveFeed';

export default function LiveMonitoring() {
  const [cameraActive, setCameraActive] = useState(false);

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Live Camera Stream</h2>
        <p className="text-xs text-slate-500">Monitor active streams and toggle individual model processing pipelines.</p>
      </div>

      {/* Live stream block */}
      <div className="max-w-6xl">
        <LiveFeed onStreamStateChange={setCameraActive} />
      </div>
    </div>
  );
}
