import React from 'react';
import { Film } from 'lucide-react';

export default function VideoPreview({ originalFile, streamActive }) {
  const [videoUrl, setVideoUrl] = React.useState(null);

  React.useEffect(() => {
    if (originalFile) {
      const url = URL.createObjectURL(originalFile);
      setVideoUrl(url);
      return () => {
        URL.revokeObjectURL(url);
      };
    } else {
      setVideoUrl(null);
    }
  }, [originalFile]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-2xl">
      {/* Original Video Player */}
      <div className="flex flex-col">
        <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Original Video Player</h4>
        <div className="bg-slate-950 rounded-lg p-2 aspect-video flex items-center justify-center border border-slate-850 overflow-hidden">
          {videoUrl ? (
            <video src={videoUrl} controls className="max-h-[300px] w-full object-contain rounded" />
          ) : (
            <span className="text-xs text-slate-700">No video selected</span>
          )}
        </div>
      </div>

      {/* Processed output video stream */}
      <div className="flex flex-col">
        <h4 className="text-xs font-bold text-purple-400 uppercase mb-3 flex items-center space-x-1.5">
          <Film className="w-4 h-4 text-purple-500 animate-pulse" />
          <span>Processed Video Stream</span>
        </h4>
        <div className="bg-slate-955 rounded-lg p-2 aspect-video flex items-center justify-center border border-purple-500/10 overflow-hidden relative">
          {streamActive ? (
            <img
              src="/api/v1/camera/stream"
              alt="Processed video stream output"
              className="max-h-[300px] w-full object-contain rounded"
              onError={(e) => {
                e.target.src = "/api/v1/camera/stream?t=" + Date.now();
              }}
            />
          ) : (
            <span className="text-xs text-slate-750">Pending video analysis...</span>
          )}
        </div>
      </div>
    </div>
  );
}
