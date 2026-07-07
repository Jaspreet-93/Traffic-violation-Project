import React, { useState, useEffect } from 'react';
import { Play, Square, Settings, Cpu } from 'lucide-react';
import { cameraAPI, pipelineAPI } from '../services/api';

export default function LiveFeed({ onStreamStateChange }) {
  const [streamActive, setStreamActive] = useState(false);
  const [sourcePath, setSourcePath] = useState('0'); // default to webcam index 0
  const [pipelineState, setPipelineState] = useState({
    tracking: false,
    helmet: false,
    plate: false,
    ocr: false,
    seatBelt: false,
    trafficLight: false,
    behavior: false,
  });

  // Query statuses on startup
  useEffect(() => {
    fetchStatuses();
  }, []);

  const fetchStatuses = async () => {
    try {
      const cam = await cameraAPI.getStatus();
      setStreamActive(cam.data.running);
      onStreamStateChange(cam.data.running);
      if (cam.data.running && cam.data.source) {
        setSourcePath(String(cam.data.source));
      }

      const tracking = await pipelineAPI.getTrackingStatus();
      const helmet = await pipelineAPI.getHelmetStatus();
      const plate = await pipelineAPI.getPlateStatus();
      const ocr = await pipelineAPI.getOCRStatus();
      const seat = await pipelineAPI.getSeatBeltStatus();
      const tl = await pipelineAPI.getTrafficLightStatus();
      const db = await pipelineAPI.getBehaviorStatus();

      setPipelineState({
        tracking: tracking.data.running,
        helmet: helmet.data.running,
        plate: plate.data.running,
        ocr: ocr.data.running,
        seatBelt: seat.data.running,
        trafficLight: tl.data.running,
        behavior: db.data.running,
      });
    } catch (err) {
      console.error("Error fetching pipeline statuses:", err);
    }
  };

  const handleStartStopStream = async () => {
    try {
      if (streamActive) {
        await cameraAPI.stopStream();
        setStreamActive(false);
        onStreamStateChange(false);
      } else {
        // Source can be camera index (integer) or video file path string
        const parsedSource = isNaN(sourcePath) ? sourcePath : parseInt(sourcePath);
        await cameraAPI.startStream(parsedSource);
        setStreamActive(true);
        onStreamStateChange(true);
      }
      // Re-fetch pipeline to synchronize statuses
      setTimeout(fetchStatuses, 1000);
    } catch (err) {
      alert("Failed to toggle camera stream: " + (err.response?.data?.detail || err.message));
    }
  };

  const toggleToggle = async (key, getStatus, start, stop) => {
    try {
      const current = pipelineState[key];
      if (current) {
        await stop();
      } else {
        await start();
      }
      setPipelineState(prev => ({ ...prev, [key]: !current }));
    } catch (err) {
      alert(`Failed to toggle ${key} detector: ` + (err.response?.data?.detail || err.message));
    }
  };

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
                : 'bg-purple-600 hover:bg-purple-700 text-white'
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
      <div className="flex-1 bg-slate-950/40 relative min-h-[350px] flex items-center justify-center">
        {streamActive ? (
          <img
            src="/api/v1/camera/stream"
            alt="Live Stream Feed"
            className="w-full h-full object-contain max-h-[500px]"
            onError={(e) => {
              // Retry on errors
              e.target.src = "/api/v1/camera/stream?t=" + Date.now();
            }}
          />
        ) : (
          <div className="text-center p-8">
            <Settings className="w-12 h-12 text-slate-700 mx-auto mb-4 animate-spin-slow" />
            <h4 className="text-slate-400 font-medium">Camera Stream Offline</h4>
            <p className="text-xs text-slate-650 mt-1">Configure your source and click "Start Stream" above to activate feed.</p>
          </div>
        )}
      </div>

      {/* Pipeline Toggles Controls Footer */}
      <div className="bg-slate-950 p-4 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[
          { key: 'tracking', label: 'Vehicle Tracking', api: pipelineAPI, get: 'getTrackingStatus', start: 'startTracking', stop: 'stopTracking' },
          { key: 'helmet', label: 'Helmet Detector', api: pipelineAPI, get: 'getHelmetStatus', start: 'startHelmet', stop: 'stopHelmet' },
          { key: 'plate', label: 'Plate Detection', api: pipelineAPI, get: 'getPlateStatus', start: 'startPlate', stop: 'stopPlate' },
          { key: 'ocr', label: 'License OCR', api: pipelineAPI, get: 'getOCRStatus', start: 'startOCR', stop: 'stopOCR' },
          { key: 'seatBelt', label: 'Seatbelt Status', api: pipelineAPI, get: 'getSeatBeltStatus', start: 'startSeatBelt', stop: 'stopSeatBelt' },
          { key: 'trafficLight', label: 'Traffic Signal', api: pipelineAPI, get: 'getTrafficLightStatus', start: 'startTrafficLight', stop: 'stopTrafficLight' },
          { key: 'behavior', label: 'Driver Behavior', api: pipelineAPI, get: 'getBehaviorStatus', start: 'startBehavior', stop: 'stopBehavior' },
        ].map((toggle) => {
          const active = pipelineState[toggle.key];
          return (
            <button
              key={toggle.key}
              disabled={!streamActive}
              onClick={() => toggleToggle(toggle.key, toggle.api[toggle.get], toggle.api[toggle.start], toggle.api[toggle.stop])}
              className={`flex items-center justify-between p-3 rounded-lg border text-left transition-all ${
                !streamActive
                  ? 'opacity-40 cursor-not-allowed border-slate-900 bg-slate-950/20 text-slate-600'
                  : active
                  ? 'border-purple-500/50 bg-purple-500/5 text-purple-400'
                  : 'border-slate-800 bg-slate-900/50 hover:bg-slate-800/80 text-slate-400'
              }`}
            >
              <span className="text-xs font-semibold">{toggle.label}</span>
              <span className={`w-2 h-2 rounded-full ${active ? 'bg-purple-500 animate-pulse' : 'bg-slate-700'}`}></span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
