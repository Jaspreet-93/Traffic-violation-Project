import React, { useRef, useState } from 'react';
import { UploadCloud, FileImage, FileVideo, AlertTriangle } from 'lucide-react';

export default function UploadArea({ onFileSelected }) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const allowedImageExts = ['.jpg', '.jpeg', '.png', '.bmp', '.webp'];
  const allowedVideoExts = ['.mp4', '.avi', '.mov', '.mkv'];

  const validateFile = (file) => {
    setErrorMsg(null);
    const name = file.name.toLowerCase();
    const size = file.size;

    const isImage = allowedImageExts.some(ext => name.endsWith(ext));
    const isVideo = allowedVideoExts.some(ext => name.endsWith(ext));

    if (!isImage && !isVideo) {
      setErrorMsg(`Unsupported file type. Please upload images (${allowedImageExts.join(', ')}) or videos (${allowedVideoExts.join(', ')}).`);
      return false;
    }

    if (isImage && size > 15 * 1024 * 1024) {
      setErrorMsg("Image size exceeds 15 MB threshold.");
      return false;
    }

    if (isVideo && size > 100 * 1024 * 1024) {
      setErrorMsg("Video size exceeds 100 MB threshold.");
      return false;
    }

    return true;
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (validateFile(file)) {
        onFileSelected(file);
      }
    }
  };

  const handleBrowse = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (validateFile(file)) {
        onFileSelected(file);
      }
    }
  };

  return (
    <div className="space-y-4">
      {errorMsg && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-450 text-xs font-semibold rounded-lg flex items-start space-x-2 leading-relaxed">
          <AlertTriangle className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center space-y-4 h-56 ${
          dragActive
            ? 'border-purple-500 bg-purple-500/5'
            : 'border-slate-800 bg-slate-900/40 hover:border-slate-700/80 hover:bg-slate-900/60'
        }`}
      >
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          accept={[...allowedImageExts, ...allowedVideoExts].join(',')}
          onChange={handleBrowse}
        />

        <div className="p-3 rounded-full bg-slate-950 text-purple-400 group-hover:scale-110 transition-transform">
          <UploadCloud className="w-8 h-8" />
        </div>

        <div className="space-y-1">
          <h4 className="text-sm font-semibold text-slate-200">Drag & Drop Traffic Image or Video</h4>
          <p className="text-[10px] text-slate-500">Supports: JPG, PNG, BMP, MP4, AVI, MOV (Max size: 100MB video / 15MB image)</p>
        </div>

        <button
          type="button"
          className="px-4 py-2 bg-purple-650 hover:bg-purple-750 text-white rounded-lg text-xs font-semibold transition-all cursor-pointer shadow-md"
        >
          Browse Files
        </button>
      </div>
    </div>
  );
}
