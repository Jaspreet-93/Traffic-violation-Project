import React, { useState } from 'react';
import { Upload, Film, Image as ImageIcon, ShieldAlert, CheckCircle } from 'lucide-react';
import { cameraAPI } from '../services/api';

export default function UploadMedia() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null); // { type, image_path, violations }
  const [videoStarted, setVideoStarted] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setAnalysisResult(null);
      setVideoStarted(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    try {
      setUploading(true);
      const res = await cameraAPI.uploadFile(selectedFile);
      
      if (res.data.type === 'video') {
        setVideoStarted(true);
        setAnalysisResult(null);
      } else if (res.data.type === 'image') {
        setAnalysisResult(res.data);
        setVideoStarted(false);
      }
    } catch (err) {
      alert("Failed to analyze file: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Upload Violation Proof</h2>
        <p className="text-xs text-slate-500">Upload photos or video clips directly to run single-frame AI evaluations or stream simulations.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: Upload card control panel */}
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
                  <Upload className="w-10 h-10 text-slate-650 group-hover:text-purple-450 transition-colors mb-2" />
                )}
                <span className="text-xs font-semibold text-slate-300 block truncate max-w-full">
                  {selectedFile ? selectedFile.name : 'Choose Image / Video'}
                </span>
                <span className="text-[10px] text-slate-600 block mt-1">Supports MP4, AVI, PNG, JPG</span>
              </div>
            </div>

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

        {/* Right Side: Visual results panel (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* 1. Video Playback Display */}
          {videoStarted && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col">
              <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
                  <Film className="w-4 h-4 text-purple-400" />
                  <span>Processing Uploaded Video Stream</span>
                </h3>
              </div>
              <div className="bg-slate-950 flex items-center justify-center p-4 min-h-[350px]">
                <img
                  src="/api/v1/camera/stream"
                  alt="Video Stream playback"
                  className="w-full h-full object-contain max-h-[450px]"
                  onError={(e) => {
                    e.target.src = "/api/v1/camera/stream?t=" + Date.now();
                  }}
                />
              </div>
            </div>
          )}

          {/* 2. Image Detection Display */}
          {analysisResult && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Processed image canvas (2 cols) */}
              <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col">
                <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                  <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-emerald-500" />
                    <span>Analyzed Output Image</span>
                  </h3>
                </div>
                <div className="bg-slate-950 flex items-center justify-center p-4">
                  <img
                    src={`/${analysisResult.image_path}`}
                    alt="Analyzed image result"
                    className="w-full h-full object-contain max-h-[450px] rounded-lg"
                  />
                </div>
              </div>

              {/* Detections sidebar logs (1 col) */}
              <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col max-h-[500px]">
                <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
                  <ShieldAlert className="w-4.5 h-4.5 text-purple-400" />
                  <span>Detected Violations</span>
                </h3>
                
                <div className="overflow-y-auto space-y-3 pr-1 flex-1">
                  {analysisResult.violations.length === 0 ? (
                    <div className="text-center p-6 text-slate-550 text-xs">
                      No violations detected in this image. Safe driving!
                    </div>
                  ) : (
                    analysisResult.violations.map((v, idx) => (
                      <div key={idx} className="bg-slate-955 border border-slate-850 p-3 rounded-lg flex items-center justify-between text-xs">
                        <div>
                          <span className="font-bold text-slate-200 block">Vehicle ID: #{v.vehicle_id}</span>
                          <span className="text-[10px] text-slate-500 font-mono">Plate: {v.plate_number || 'UNKNOWN'}</span>
                        </div>
                        <div className="text-right">
                          <span className="text-[10px] font-bold uppercase text-purple-450 bg-purple-500/5 px-2 py-0.5 rounded border border-purple-500/10">
                            {v.violation_type}
                          </span>
                          <span className="text-[9px] text-slate-500 block mt-1">Conf: {(v.confidence * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Placeholders if no media is selected */}
          {!videoStarted && !analysisResult && (
            <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-12 text-center text-slate-500 flex flex-col items-center justify-center min-h-[350px]">
              <ImageIcon className="w-12 h-12 text-slate-850 mb-3" />
              <h4 className="text-slate-400 font-medium">No Active Results Display</h4>
              <p className="text-xs text-slate-650 mt-1">Choose a photo or video file on the left and click submit to trigger detections.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
