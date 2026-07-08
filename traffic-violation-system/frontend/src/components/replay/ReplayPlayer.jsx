import React, { useRef, useState, useEffect } from 'react';
import { Video, ShieldAlert } from 'lucide-react';

export default function ReplayPlayer({ videoUrl, speed = 1.0, isPlaying = false, onProgressUpdate }) {
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

  const handleTimeUpdate = () => {
    if (videoRef.current && onProgressUpdate) {
      const current = videoRef.current.currentTime;
      const duration = videoRef.current.duration || 1.0;
      onProgressUpdate((current / duration) * 100);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg space-y-4 p-5">
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

      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center min-h-[300px]">
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
    </div>
  );
}
