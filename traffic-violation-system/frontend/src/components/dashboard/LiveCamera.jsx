import React from 'react';
import { Play, Square, Settings, Cpu } from 'lucide-react';

export default function LiveCamera({
  streamActive,
  sourcePath,
  setSourcePath,
  handleStartStopStream,
  pipelineState,
  toggleToggle,
  streamURL = "/api/v1/camera/stream"
}) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col h-full">
      {/* Stream Display header */}
      <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Cpu className="w-5 h-5 text-purple-500 animate-pulse" />
          <h3 className="font-semibold text-sm text-slate-200">Real-Time Camera Stream</h3>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="text"
            value={sourcePath}
            onChange={(e) => setSourcePath(e.target.value)}
            disabled={streamActive}
            placeholder="0 or video.mp4"
            className="bg-slate-900 border border-slate-800 text-xs px-3 py-1.5 rounded-lg text-slate-300 w-32 focus:outline-none focus:border-purple-500 disabled:opacity-50"
          />
          <button
            onClick={handleStartStopStream}
            className={`flex items-center space-x-1.5 text-xs font-semibold px-4 py-1.5 rounded-lg transition-all ${
              streamActive
                ? 'bg-rose-600 hover:bg-rose-700 text-white'
                : 'bg-purple-650 hover:bg-purple-755 text-white'
            }`}
          >
            {streamActive ? (
              <>
                <Square className="w-3.5 h-3.5" />
                <span>Stop</span>
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5" />
                <span>Start Stream</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Video Stream Frame Canvas */}
      <div className="flex-1 bg-slate-955 relative min-h-[350px] flex items-center justify-center">
        {streamActive ? (
          <img
            src={streamURL}
            alt="Live Stream Feed"
            className="w-full h-full object-contain max-h-[500px]"
            onError={(e) => {
              e.target.src = streamURL + "?t=" + Date.now();
            }}
          />
        ) : (
          <div className="text-center p-8">
            <Settings className="w-12 h-12 text-slate-700 mx-auto mb-4 animate-spin-slow" />
            <h4 className="text-slate-450 font-medium">Camera Stream Offline</h4>
            <p className="text-xs text-slate-600 mt-1">Configure your source and click "Start Stream" above to activate feed.</p>
          </div>
        )}
      </div>

      {/* Pipeline Toggles Controls Footer */}
      {pipelineState && toggleToggle && (
        <div className="bg-slate-950 p-4 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {pipelineState.map((toggle) => (
            <button
              key={toggle.key}
              disabled={!streamActive}
              onClick={() => toggleToggle(toggle)}
              className={`flex items-center justify-between p-3 rounded-lg border text-left transition-all ${
                !streamActive
                  ? 'opacity-40 cursor-not-allowed border-slate-900 bg-slate-950/20 text-slate-650'
                  : toggle.active
                  ? 'border-purple-500/50 bg-purple-500/5 text-purple-450'
                  : 'border-slate-800 bg-slate-900/50 hover:bg-slate-800/80 text-slate-450'
              }`}
            >
              <span className="text-xs font-semibold">{toggle.label}</span>
              <span className={`w-2 h-2 rounded-full ${toggle.active ? 'bg-purple-500 animate-pulse' : 'bg-slate-700'}`}></span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
