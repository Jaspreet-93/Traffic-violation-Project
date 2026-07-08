import React from 'react';
import { Upload, Film, Image as ImageIcon } from 'lucide-react';

export default function FileUploader({
  selectedFile,
  handleFileChange,
  handleUpload,
  uploading
}) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col h-fit">
      <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
        <Upload className="w-4.5 h-4.5 text-purple-400" />
        <span>Select Local Media</span>
      </h3>

      <form onSubmit={handleUpload} className="space-y-4">
        <div className="border border-dashed border-slate-850 hover:border-purple-500/50 bg-slate-950/20 hover:bg-slate-950/40 py-10 px-4 rounded-xl text-center transition-all cursor-pointer relative group">
          <input
            type="file"
            accept="image/*,video/*"
            onChange={handleFileChange}
            className="absolute inset-0 opacity-0 cursor-pointer"
          />
          <div className="flex flex-col items-center justify-center">
            {selectedFile ? (
              selectedFile.type.startsWith('video') ? (
                <Film className="w-10 h-10 text-purple-400 mb-2 animate-pulse" />
              ) : (
                <ImageIcon className="w-10 h-10 text-purple-400 mb-2 animate-pulse" />
              )
            ) : (
              <Upload className="w-10 h-10 text-slate-650 group-hover:text-purple-455 transition-colors mb-2" />
            )}
            <span className="text-xs font-semibold text-slate-300 block truncate max-w-full">
              {selectedFile ? selectedFile.name : 'Choose Image / Video'}
            </span>
            <span className="text-[10px] text-slate-600 block mt-1">Supports MP4, AVI, PNG, JPG</span>
          </div>
        </div>

        {uploading && (
          <div className="w-full bg-slate-950 rounded-full h-1.5 overflow-hidden">
            <div className="bg-purple-500 h-1.5 rounded-full animate-progress" style={{ width: '80%' }}></div>
          </div>
        )}

        <button
          type="submit"
          disabled={!selectedFile || uploading}
          className="w-full bg-purple-650 hover:bg-purple-750 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold py-2.5 rounded-xl transition-all shadow text-xs flex items-center justify-center space-x-2"
        >
          {uploading ? (
            <>
              <span className="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin"></span>
              <span>Analyzing...</span>
            </>
          ) : (
            <span>Upload & Run Detections</span>
          )}
        </button>
      </form>
    </div>
  );
}
