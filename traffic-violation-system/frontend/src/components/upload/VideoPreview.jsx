import React from 'react';
import { Play, FileVideo } from 'lucide-react';

export default function VideoPreview({ file, onClear }) {
  if (!file) return null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-4 shadow">
      <div className="flex items-center justify-between text-xs">
        <span className="text-slate-400 flex items-center space-x-1.5 font-semibold">
          <FileVideo className="w-4 h-4 text-purple-400" />
          <span>Video Source Preview</span>
        </span>
        <button
          onClick={onClear}
          className="text-slate-500 hover:text-slate-350 font-bold uppercase text-[10px]"
        >
          Remove
        </button>
      </div>

      <div className="rounded-lg overflow-hidden border border-slate-850 bg-slate-950 flex items-center justify-center max-h-80">
        <video
          src={URL.createObjectURL(file)}
          controls
          className="object-contain max-h-80 w-full"
        />
      </div>

      <div className="flex items-center justify-between text-[10px] text-slate-500 font-mono">
        <span>File: {file.name}</span>
        <span>Size: {(file.size / (1024*1024)).toFixed(2)} MB</span>
      </div>
    </div>
  );
}
