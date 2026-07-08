import React from 'react';

export default function Loader() {
  return (
    <div className="flex flex-col items-center justify-center space-y-3 p-8">
      <span className="relative flex h-10 w-10">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-purple-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-10 w-10 bg-purple-650 border border-purple-500 border-t-transparent animate-spin"></span>
      </span>
      <span className="text-xs text-slate-500 font-medium">Processing stream frame data...</span>
    </div>
  );
}
