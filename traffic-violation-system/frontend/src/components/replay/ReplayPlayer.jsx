import React, { useRef, useState, useEffect } from 'react';
import { Video, ShieldAlert, Play, Pause, Square, SkipBack, SkipForward } from 'lucide-react';

export default function ReplayPlayer({
  videoUrl,
  speed = 1.0,
  isPlaying = false,
  progress = 0.0,
  onProgressUpdate,
  onTogglePlay,
  onStop,
  onFrameBack,
  onFrameForward,
  onSpeedChange
}) {
  const videoRef = useRef(null);
  const [useProcessed, setUseProcessed] = useState(true);

  // Sync speed and play state
  useEffect(() => {
    if (!videoRef.current) return;
    videoRef.current.playbackRate = speed;
    if (isPlaying) {
      videoRef.current.play().catch(() => {});
    } else {
      videoRef.current.pause();
    }
  }, [speed, isPlaying, videoUrl]);

  // Handle video element timeupdate to update progress bar
  const handleTimeUpdate = () => {
    if (videoRef.current && onProgressUpdate) {
      const current = videoRef.current.currentTime;
      const duration = videoRef.current.duration || 1.0;
      onProgressUpdate((current / duration) * 100);
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
          src={videoUrl}
          onTimeUpdate={handleTimeUpdate}
          className="w-full object-contain max-h-[400px]"
        />
        {useProcessed && (
          <div className="absolute top-3 left-3 bg-rose-500/10 border border-rose-500/20 text-rose-450 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
            <ShieldAlert className="w-3 h-3 animate-pulse" />
            <span>AI Bounding Boxes Active</span>
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
