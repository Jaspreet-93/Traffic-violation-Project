import React, { useState, useEffect } from 'react';
import { Upload, Camera, Film, Image as ImageIcon, CheckCircle, ShieldAlert } from 'lucide-react';
import LiveFeed from '../components/LiveFeed';
import { cameraAPI } from '../services/api';

export default function LiveMonitoring() {
  const [cameraActive, setCameraActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null); // { type, image_path, violations }
  const [activeTab, setActiveTab] = useState('live'); // 'live' or 'upload_result'

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setAnalysisResult(null); // clear previous results
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    try {
      setUploading(true);
      const res = await cameraAPI.uploadFile(selectedFile);
      
      if (res.data.type === 'video') {
        alert("Video upload successful. Playing video stream...");
        setAnalysisResult(null);
        setActiveTab('live');
        setCameraActive(true);
        // Force refresh key by querying status
        window.location.reload();
      } else if (res.data.type === 'image') {
        setAnalysisResult(res.data);
        setActiveTab('upload_result');
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
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-100">Live Camera Stream</h2>
          <p className="text-xs text-slate-500">Monitor active feeds, toggle detectors, or upload files to evaluate infractions.</p>
        </div>

        {/* Tab options selector */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1.5 rounded-xl">
          <button
            onClick={() => setActiveTab('live')}
            className={`flex items-center space-x-1.5 px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
              activeTab === 'live'
                ? 'bg-purple-650 text-white shadow'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Camera className="w-3.5 h-3.5" />
            <span>Live Stream</span>
          </button>
          {analysisResult && (
            <button
              onClick={() => setActiveTab('upload_result')}
              className={`flex items-center space-x-1.5 px-4 py-2 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'upload_result'
                  ? 'bg-purple-650 text-white shadow'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <ImageIcon className="w-3.5 h-3.5" />
              <span>Image Analysis Result</span>
            </button>
          )}
        </div>
      </div>

      {/* Main panels */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stream / Image result panel (2 cols) */}
        <div className="lg:col-span-2">
          {activeTab === 'live' ? (
            <LiveFeed onStreamStateChange={setCameraActive} />
          ) : (
            analysisResult && (
              <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-2xl flex flex-col">
                <div className="bg-slate-950 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                  <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-emerald-500" />
                    <span>Analyzed Image Result</span>
                  </h3>
                  <button
                    onClick={() => {
                      setAnalysisResult(null);
                      setActiveTab('live');
                    }}
                    className="text-xs text-slate-450 hover:text-slate-250 font-medium"
                  >
                    Back to Live Feed
                  </button>
                </div>
                <div className="bg-slate-950 flex items-center justify-center p-4">
                  <img
                    src={`/${analysisResult.image_path}`}
                    alt="Analyzed snapshot"
                    className="w-full h-full object-contain max-h-[500px] rounded-lg"
                  />
                </div>
              </div>
            )
          )}
        </div>

        {/* Upload panel & Analysis Logs (1 col) */}
        <div className="space-y-6">
          {/* File uploader Card */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col">
            <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
              <Upload className="w-4.5 h-4.5 text-purple-400" />
              <span>Upload Proof File</span>
            </h3>

            <form onSubmit={handleUpload} className="space-y-4">
              <div className="border border-dashed border-slate-800 hover:border-purple-550 bg-slate-955/40 hover:bg-slate-950/20 py-8 px-4 rounded-xl text-center transition-all cursor-pointer relative group">
                <input
                  type="file"
                  accept="image/*,video/*"
                  onChange={handleFileChange}
                  className="absolute inset-0 opacity-0 cursor-pointer"
                />
                <div className="flex flex-col items-center justify-center">
                  {selectedFile ? (
                    selectedFile.type.startsWith('video') ? (
                      <Film className="w-10 h-10 text-purple-400 mb-2" />
                    ) : (
                      <ImageIcon className="w-10 h-10 text-purple-400 mb-2" />
                    )
                  ) : (
                    <Upload className="w-10 h-10 text-slate-650 group-hover:text-purple-450 transition-colors mb-2" />
                  )}
                  <span className="text-xs font-semibold text-slate-350 block truncate max-w-full">
                    {selectedFile ? selectedFile.name : 'Choose Image / Video'}
                  </span>
                  <span className="text-[10px] text-slate-600 block mt-1">PNG, JPG, MP4, AVI formats</span>
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
                  <span>Upload & Analyze</span>
                )}
              </button>
            </form>
          </div>

          {/* Detections log list (if image analyzed) */}
          {activeTab === 'upload_result' && analysisResult && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col max-h-[350px]">
              <h3 className="font-semibold text-sm text-slate-200 mb-4 flex items-center space-x-2">
                <ShieldAlert className="w-4.5 h-4.5 text-purple-400" />
                <span>Detected Infractions</span>
              </h3>
              
              <div className="overflow-y-auto space-y-3 pr-1 flex-1">
                {analysisResult.violations.length === 0 ? (
                  <div className="text-center p-6 text-slate-550 text-xs">
                    No violations detected in this image. Safe driving!
                  </div>
                ) : (
                  analysisResult.violations.map((v, idx) => (
                    <div key={idx} className="bg-slate-950 border border-slate-850 p-3 rounded-lg flex items-center justify-between text-xs">
                      <div>
                        <span className="font-bold text-slate-200 block">Vehicle ID: #{v.vehicle_id}</span>
                        <span className="text-[10px] text-slate-500 font-mono">Plate: {v.plate_number || 'UNKNOWN'}</span>
                      </div>
                      <div className="text-right">
                        <span className="text-[10px] font-bold uppercase text-purple-400 bg-purple-500/5 px-2 py-0.5 rounded border border-purple-500/10">
                          {v.violation_type}
                        </span>
                        <span className="text-[9px] text-slate-500 block mt-1">Conf: {(v.confidence * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
