import React, { useRef, useState, useEffect } from 'react';
import { Video, ShieldAlert, Play, Pause, Square, SkipBack, SkipForward } from 'lucide-react';

export default function ReplayPlayer({
  processedVideoUrl,
  originalVideoUrl,
  speed = 1.0,
  isPlaying = false,
  progress = 0.0,
  timeline = [],
  onProgressUpdate,
  onTogglePlay,
  onStop,
  onFrameBack,
  onFrameForward,
  onSpeedChange
}) {
  const videoRef = useRef(null);
  const [useProcessed, setUseProcessed] = useState(true);
  const triggeredRef = useRef(new Set());
  const [slowToast, setSlowToast] = useState(null);

  // Sync speed and play state
  useEffect(() => {
    if (!videoRef.current) return;
    videoRef.current.playbackRate = speed;
    if (isPlaying) {
      videoRef.current.play().catch(() => {});
    } else {
      videoRef.current.pause();
    }
  }, [speed, isPlaying, useProcessed, processedVideoUrl, originalVideoUrl]);

  const isAutoSlowedRef = useRef(false);

  // Clear triggers when video is stopped or starts over
  useEffect(() => {
    if (!isPlaying && progress === 0) {
      triggeredRef.current.clear();
      isAutoSlowedRef.current = false;
    }
  }, [isPlaying, progress]);

  // Handle video element timeupdate to update progress bar
  const handleTimeUpdate = () => {
    if (videoRef.current && onProgressUpdate) {
      const current = videoRef.current.currentTime;
      const duration = videoRef.current.duration || 1.0;
      onProgressUpdate((current / duration) * 100);

      // Auto-slowdown feature when a violation is detected in timeline!
      if (timeline && timeline.length > 0) {
        // Find if there is any violation event currently active (within 1.2s of playback head)
        const activeEvent = timeline.find(event => Math.abs(current - event.time_offset_sec) < 1.2);

        if (activeEvent) {
          // If a violation is active and speed is normal, slow down!
          if (speed >= 1.0 && !triggeredRef.current.has(activeEvent.time_offset_sec)) {
            triggeredRef.current.add(activeEvent.time_offset_sec);
            isAutoSlowedRef.current = true;
            if (onSpeedChange) {
              onSpeedChange(0.25); // Slow down to 0.25x
            }
            setSlowToast(`⚠️ Auto-Slowing (0.25x): Violation Detected!`);
            setTimeout(() => setSlowToast(null), 3000);
          }
        } else {
          // If no violation is active, but we were auto-slowed, automatically restore to normal speed!
          if (isAutoSlowedRef.current) {
            isAutoSlowedRef.current = false;
            if (onSpeedChange) {
              onSpeedChange(1.0); // Restore to 1.0x
            }
            setSlowToast(`✅ Restoring Normal Speed (1.0x)`);
            setTimeout(() => setSlowToast(null), 2000);
          }
        }
      }
    }
  };

  // Handle user scrubbing the progress bar
  const handleProgressChange = (e) => {
    const val = parseFloat(e.target.value);
    if (videoRef.current) {
      const duration = videoRef.current.duration || 1.0;
      videoRef.current.currentTime = (val / 100) * duration;
    }
    if (onProgressUpdate) {
      onProgressUpdate(val);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg p-5 space-y-4">
      {/* Title Header */}
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-slate-200 flex items-center space-x-2">
          <Video className="w-4.5 h-4.5 text-purple-400" />
          <span>Surveillance Footage Playback Canvas</span>
        </h3>
        
        {/* Toggle processed vs original */}
        <div className="flex items-center bg-slate-950 border border-slate-850 p-1 rounded-lg">
          <button
            onClick={() => setUseProcessed(true)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all ${
              useProcessed ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Processed
          </button>
          <button
            onClick={() => setUseProcessed(false)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all ${
              !useProcessed ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Original
          </button>
        </div>
      </div>

      {/* Screen */}
      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-955 flex items-center justify-center min-h-[300px]">
        <video
          ref={videoRef}
          src={useProcessed ? processedVideoUrl : originalVideoUrl}
          onTimeUpdate={handleTimeUpdate}
          className="w-full object-contain max-h-[400px]"
        />
        {useProcessed && (
          <div className="absolute top-3 left-3 bg-rose-500/10 border border-rose-500/20 text-rose-450 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
            <ShieldAlert className="w-3 h-3 animate-pulse" />
            <span>AI Bounding Boxes Active</span>
          </div>
        )}
        {slowToast && (
          <div className="absolute bottom-3 left-3 bg-purple-650/90 border border-purple-550 text-white text-[10px] font-bold px-3 py-1.5 rounded-lg shadow-lg flex items-center space-x-1.5 animate-bounce">
            <span>{slowToast}</span>
          </div>
        )}
      </div>

      {/* Timeline Slider */}
      <div className="space-y-1">
        <div className="relative w-full h-1.5 bg-slate-955 rounded-full overflow-hidden border border-slate-850">
          <input
            type="range"
            min="0"
            max="100"
            step="0.1"
            value={progress}
            onChange={handleProgressChange}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
          />
          <div
            className="bg-purple-650 h-full rounded-full transition-all duration-100"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-[10px] text-slate-500 font-mono">
          <span>00:00</span>
          <span>Progress: {progress.toFixed(0)}%</span>
          <span>Duration: 15.0s</span>
        </div>
      </div>

      {/* Playback Controls & Speed Controls Panel */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-slate-850">
        <div className="flex items-center space-x-2">
          {/* Play/Pause */}
          <button onClick={onTogglePlay} className="p-2 rounded-lg bg-slate-955 border border-slate-850 text-slate-350 hover:text-purple-400 hover:bg-slate-900/60 transition-all cursor-pointer" title={isPlaying ? "Pause" : "Play"}>
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </button>

          {/* Stop */}
          <button onClick={onStop} className="p-2 rounded-lg bg-slate-955 border border-slate-850 text-slate-350 hover:text-purple-400 hover:bg-slate-900/60 transition-all cursor-pointer" title="Stop">
            <Square className="w-4 h-4" />
          </button>

          <div className="h-6 w-[1px] bg-slate-800"></div>

          {/* Frame skip */}
          <button onClick={onFrameBack} className="p-2 rounded-lg bg-slate-955 border border-slate-850 text-slate-350 hover:text-purple-400 hover:bg-slate-900/60 transition-all cursor-pointer" title="Frame Back">
            <SkipBack className="w-4 h-4" />
          </button>
          <button onClick={onFrameForward} className="p-2 rounded-lg bg-slate-955 border border-slate-850 text-slate-350 hover:text-purple-400 hover:bg-slate-900/60 transition-all cursor-pointer" title="Frame Forward">
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        {/* Speed */}
        <div className="flex items-center space-x-3">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Speed:</span>
          <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
            {[0.25, 0.5, 1.0, 1.5, 2.0].map((s) => (
              <button
                key={s}
                onClick={() => onSpeedChange(s)}
                className={`px-2.5 py-1 rounded text-[9px] font-bold transition-all cursor-pointer ${
                  speed === s ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                }`}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
