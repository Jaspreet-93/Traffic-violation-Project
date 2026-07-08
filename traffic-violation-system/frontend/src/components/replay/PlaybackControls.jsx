import React from 'react';
import { Play, Pause, Square, SkipBack, SkipForward, Maximize } from 'lucide-react';

export default function PlaybackControls({ isPlaying, onTogglePlay, onStop, onFrameBack, onFrameForward, onFullscreen }) {
  const btnClass = "p-2 rounded-lg bg-slate-950 border border-slate-850 text-slate-350 hover:text-purple-400 hover:bg-slate-900/60 transition-all cursor-pointer";

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow flex items-center justify-between">
      <div className="flex items-center space-x-2.5">
        {/* Play/Pause */}
        <button onClick={onTogglePlay} className={btnClass} title={isPlaying ? "Pause" : "Play"}>
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </button>

        {/* Stop */}
        <button onClick={onStop} className={btnClass} title="Stop">
          <Square className="w-4 h-4" />
        </button>

        <div className="h-6 w-[1px] bg-slate-800"></div>

        {/* Frame by Frame */}
        <button onClick={onFrameBack} className={btnClass} title="Frame Back">
          <SkipBack className="w-4 h-4" />
        </button>
        <button onClick={onFrameForward} className={btnClass} title="Frame Forward">
          <SkipForward className="w-4 h-4" />
        </button>
      </div>

      {/* Fullscreen */}
      <button onClick={onFullscreen} className={btnClass} title="Fullscreen">
        <Maximize className="w-4 h-4" />
      </button>
    </div>
  );
}
