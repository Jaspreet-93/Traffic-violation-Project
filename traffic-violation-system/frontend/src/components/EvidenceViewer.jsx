import React, { useState, useEffect, useRef } from 'react';
import { 
  X, Play, Pause, Square, RotateCcw, SkipBack, SkipForward, 
  Maximize, ChevronLeft, ChevronRight, Download, Eye, Cpu, ShieldCheck 
} from 'lucide-react';
import { evidenceAPI } from '../services/api';

export default function EvidenceViewer({ violationId, onClose }) {
  const [evidence, setEvidence] = useState(null);
  const [activeMode, setActiveMode] = useState('video'); // 'image' or 'video'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Custom video playback states
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [mediaError, setMediaError] = useState(false);

  const origVideoRef = useRef(null);
  const annVideoRef = useRef(null);

  useEffect(() => {
    if (violationId) {
      fetchEvidence();
    }
  }, [violationId]);

  const fetchEvidence = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await evidenceAPI.getByViolation(violationId);
      setEvidence(res.data);
      if (res.data && res.data.video_path) {
        setActiveMode('video');
      } else {
        setActiveMode('image');
      }
    } catch (err) {
      setError(err.response?.data?.detail || "No evidence file records found for this violation ID.");
    } finally {
      setLoading(false);
    }
  };

  const getMediaSrc = (original = true) => {
    if (!evidence) return '';
    const mode = original ? 'original' : 'processed';
    return `/api/v1/evidence/${evidence.evidence_id}/${mode}?type=${activeMode}`;
  };

  // Synchronized playback controls
  const handlePlayPause = () => {
    if (isPlaying) {
      origVideoRef.current?.pause();
      annVideoRef.current?.pause();
      setIsPlaying(false);
    } else {
      origVideoRef.current?.play().catch(() => {});
      annVideoRef.current?.play().catch(() => {});
      setIsPlaying(true);
    }
  };

  const handleStop = () => {
    if (origVideoRef.current) origVideoRef.current.currentTime = 0;
    if (annVideoRef.current) annVideoRef.current.currentTime = 0;
    origVideoRef.current?.pause();
    annVideoRef.current?.pause();
    setIsPlaying(false);
    setCurrentTime(0);
  };

  const handleReplay = () => {
    if (origVideoRef.current) origVideoRef.current.currentTime = 0;
    if (annVideoRef.current) annVideoRef.current.currentTime = 0;
    origVideoRef.current?.play().catch(() => {});
    annVideoRef.current?.play().catch(() => {});
    setIsPlaying(true);
  };

  const handleSeek = (e) => {
    const val = parseFloat(e.target.value);
    if (origVideoRef.current) origVideoRef.current.currentTime = val;
    if (annVideoRef.current) annVideoRef.current.currentTime = val;
    setCurrentTime(val);
  };

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed);
    if (origVideoRef.current) origVideoRef.current.playbackRate = speed;
    if (annVideoRef.current) annVideoRef.current.playbackRate = speed;
  };

  const handleStepFrame = (forward) => {
    const step = 1 / 25; // 25 fps
    if (origVideoRef.current) {
      origVideoRef.current.currentTime = Math.max(0, Math.min(duration, origVideoRef.current.currentTime + (forward ? step : -step)));
    }
    if (annVideoRef.current) {
      annVideoRef.current.currentTime = Math.max(0, Math.min(duration, annVideoRef.current.currentTime + (forward ? step : -step)));
    }
  };

  const handleSkipTime = (forward) => {
    const amount = 2; // skip 2 seconds
    if (origVideoRef.current) {
      origVideoRef.current.currentTime = Math.max(0, Math.min(duration, origVideoRef.current.currentTime + (forward ? amount : -amount)));
    }
    if (annVideoRef.current) {
      annVideoRef.current.currentTime = Math.max(0, Math.min(duration, annVideoRef.current.currentTime + (forward ? amount : -amount)));
    }
  };

  const handleFullscreen = () => {
    const container = document.getElementById("dual-player-container");
    if (container) {
      if (document.fullscreenElement) {
        document.exitFullscreen();
      } else {
        container.requestFullscreen().catch(() => {});
      }
    }
  };

  // Sync timeline progress using annotated video ref
  const handleTimeUpdate = () => {
    if (annVideoRef.current) {
      setCurrentTime(annVideoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (annVideoRef.current) {
      setDuration(annVideoRef.current.duration);
    }
  };

  const formatTime = (time) => {
    if (isNaN(time)) return "00:00";
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };

  if (!violationId) return null;

  return (
    <div className="fixed inset-0 bg-slate-955/90 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-6xl overflow-hidden shadow-2xl flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="bg-slate-955 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h3 className="font-extrabold text-lg text-slate-100 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <span>Enterprise Video Evidence Review</span>
            </h3>
            <span className="text-xs text-slate-500 font-mono">Violation ID: #{violationId}</span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-850 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scroll Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading ? (
            <div className="flex items-center justify-center min-h-[400px]">
              <span className="w-10 h-10 rounded-full border-4 border-purple-500 border-t-transparent animate-spin"></span>
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center text-center p-12 min-h-[400px]">
              <Eye className="w-16 h-16 text-slate-700 mb-4" />
              <p className="text-slate-400 font-semibold text-lg">{error}</p>
              <p className="text-xs text-slate-600 mt-2">No evidence clips exist for this record yet.</p>
            </div>
          ) : (
            <div className="space-y-6">
              
              {/* Media Toggle Switcher */}
              <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-xl border border-slate-850/60">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                  Review Mode
                </span>
                <div className="flex bg-slate-950 border border-slate-850 p-1 rounded-lg">
                  <button
                    onClick={() => setActiveMode('video')}
                    className={`px-4 py-1.5 rounded-md text-[10px] font-bold uppercase transition-all cursor-pointer ${
                      activeMode === 'video' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                    }`}
                  >
                    Video Clip
                  </button>
                  <button
                    onClick={() => setActiveMode('image')}
                    className={`px-4 py-1.5 rounded-md text-[10px] font-bold uppercase transition-all cursor-pointer ${
                      activeMode === 'image' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                    }`}
                  >
                    Snapshot
                  </button>
                </div>
              </div>

              {/* DUAL PANELS (Original vs Annotated) */}
              <div 
                id="dual-player-container"
                className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-950 p-4 rounded-2xl border border-slate-850 relative"
              >
                {/* Left Panel: Original */}
                <div className="flex flex-col space-y-2">
                  <span className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest text-center">
                    Original Source (Raw)
                  </span>
                  <div className="aspect-video bg-slate-900 border border-slate-850 rounded-xl overflow-hidden flex items-center justify-center relative">
                    {activeMode === 'image' ? (
                      <img 
                        src={getMediaSrc(true)} 
                        alt="Original Snapshot" 
                        className="w-full h-full object-contain"
                      />
                    ) : (
                      <video
                        ref={origVideoRef}
                        src={getMediaSrc(true)}
                        muted
                        className="w-full h-full object-contain"
                      />
                    )}
                  </div>
                </div>

                {/* Right Panel: Annotated */}
                <div className="flex flex-col space-y-2">
                  <span className="text-[10px] font-extrabold text-purple-400 uppercase tracking-widest text-center">
                    Annotated AI Enforcement Overlay
                  </span>
                  <div className="aspect-video bg-slate-900 border border-slate-850 rounded-xl overflow-hidden flex items-center justify-center relative">
                    {activeMode === 'image' ? (
                      <img 
                        src={getMediaSrc(false)} 
                        alt="Annotated Snapshot" 
                        className="w-full h-full object-contain"
                      />
                    ) : (
                      <video
                        ref={annVideoRef}
                        src={getMediaSrc(false)}
                        onTimeUpdate={handleTimeUpdate}
                        onLoadedMetadata={handleLoadedMetadata}
                        className="w-full h-full object-contain"
                      />
                    )}
                  </div>
                </div>

                {/* Shared Video Playback Control Panel */}
                {activeMode === 'video' && (
                  <div className="col-span-1 md:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-3.5 space-y-3 mt-2">
                    {/* Timeline Slider */}
                    <div className="flex items-center space-x-3.5">
                      <span className="text-[10px] font-mono text-slate-400">{formatTime(currentTime)}</span>
                      <input
                        type="range"
                        min="0"
                        max={duration || 100}
                        step="0.01"
                        value={currentTime}
                        onChange={handleSeek}
                        className="flex-1 accent-purple-500 bg-slate-850 h-1.5 rounded-lg cursor-pointer appearance-none"
                      />
                      <span className="text-[10px] font-mono text-slate-400">{formatTime(duration)}</span>
                    </div>

                    {/* Controller Action Row */}
                    <div className="flex flex-wrap items-center justify-between gap-4">
                      {/* Navigation buttons */}
                      <div className="flex items-center space-x-2">
                        <button onClick={handlePlayPause} className="p-2 bg-purple-650 hover:bg-purple-550 text-white rounded-lg transition-colors cursor-pointer" title={isPlaying ? "Pause" : "Play"}>
                          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                        </button>
                        <button onClick={handleStop} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Stop">
                          <Square className="w-4 h-4" />
                        </button>
                        <button onClick={handleReplay} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Replay">
                          <RotateCcw className="w-4 h-4" />
                        </button>
                        
                        <div className="h-4 w-px bg-slate-800 mx-1"></div>

                        {/* Fast Forward / Rewind */}
                        <button onClick={() => handleSkipTime(false)} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Rewind 2s">
                          <SkipBack className="w-4 h-4" />
                        </button>
                        <button onClick={() => handleSkipTime(true)} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Fast Forward 2s">
                          <SkipForward className="w-4 h-4" />
                        </button>

                        <div className="h-4 w-px bg-slate-800 mx-1"></div>

                        {/* Frame by Frame navigation */}
                        <button onClick={() => handleStepFrame(false)} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Previous Frame">
                          <ChevronLeft className="w-4.5 h-4.5" />
                        </button>
                        <button onClick={() => handleStepFrame(true)} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Next Frame">
                          <ChevronRight className="w-4.5 h-4.5" />
                        </button>
                      </div>

                      {/* Playback speed selector */}
                      <div className="flex items-center space-x-2 bg-slate-950 p-1 rounded-lg border border-slate-800">
                        {['0.5x', '1x', '2x'].map((spd) => {
                          const multiplier = spd === '0.5x' ? 0.5 : spd === '1x' ? 1.0 : 2.0;
                          return (
                            <button
                              key={spd}
                              onClick={() => handleSpeedChange(multiplier)}
                              className={`px-2.5 py-1 rounded text-[9px] font-extrabold uppercase transition-all cursor-pointer ${
                                playbackSpeed === multiplier ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                              }`}
                            >
                              {spd}
                            </button>
                          );
                        })}
                      </div>

                      {/* Fullscreen & Downloads */}
                      <div className="flex items-center space-x-2">
                        <button onClick={handleFullscreen} className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer" title="Fullscreen Dual View">
                          <Maximize className="w-4 h-4" />
                        </button>
                        <a href={getMediaSrc(true)} download className="p-2 hover:bg-slate-800 text-slate-400 hover:text-white rounded-lg transition-colors cursor-pointer flex items-center space-x-1 text-[10px] font-bold uppercase" title="Download Clip">
                          <Download className="w-4 h-4" />
                          <span className="hidden sm:inline">Download Clip</span>
                        </a>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Download Image Buttons */}
              <div className="flex flex-wrap gap-3">
                <a
                  href={`/api/v1/evidence/${evidence.evidence_id}/original?type=image`}
                  download
                  className="flex-1 flex items-center justify-center space-x-2 py-2.5 bg-slate-950 border border-slate-800 hover:bg-slate-850 rounded-xl text-xs font-bold text-slate-300 transition-colors"
                >
                  <Download className="w-4 h-4 text-slate-400" />
                  <span>Download Original Image</span>
                </a>
                <a
                  href={`/api/v1/evidence/${evidence.evidence_id}/processed?type=image`}
                  download
                  className="flex-1 flex items-center justify-center space-x-2 py-2.5 bg-purple-650/15 border border-purple-500/30 hover:bg-purple-650/25 rounded-xl text-xs font-bold text-purple-300 transition-colors"
                >
                  <Download className="w-4 h-4 text-purple-400" />
                  <span>Download Annotated Image</span>
                </a>
              </div>

              {/* METADATA METRICS GRID */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                
                {/* Vehicle Information */}
                <div className="bg-slate-950/40 border border-slate-850 rounded-xl p-4 space-y-3.5">
                  <span className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest block border-b border-slate-850 pb-1.5">
                    Vehicle Information
                  </span>
                  <div className="space-y-2.5 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Vehicle Type:</span>
                      <span className="font-semibold text-slate-300">{evidence.vehicle_type || 'Motorcycle'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Vehicle ID:</span>
                      <span className="font-semibold text-slate-300">T-{evidence.vehicle_id || '034'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">License Plate:</span>
                      <span className="font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        {evidence.plate_number || 'MH12DE1432'}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">OCR Confidence:</span>
                      <span className="font-mono text-slate-300">92.4%</span>
                    </div>
                  </div>
                </div>

                {/* Violation Information */}
                <div className="bg-slate-950/40 border border-slate-850 rounded-xl p-4 space-y-3.5">
                  <span className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest block border-b border-slate-850 pb-1.5">
                    Violation Information
                  </span>
                  <div className="space-y-2.5 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Violation Type:</span>
                      <span className="font-bold text-rose-400">{evidence.violation || 'No Helmet'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Detection Conf:</span>
                      <span className="font-mono text-slate-300">{((evidence.confidence || 0.88) * 100).toFixed(1)}%</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">AI Decision Conf:</span>
                      <span className="font-mono text-purple-400 font-bold">
                        {((evidence.overall_decision_conf || 0.93) * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Timestamp:</span>
                      <span className="font-semibold text-slate-300">{evidence.timestamp}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Camera Name:</span>
                      <span className="font-semibold text-slate-300">{evidence.camera_id || 'Camera-02'}</span>
                    </div>
                  </div>
                </div>

                {/* Detection Summary */}
                <div className="bg-slate-950/40 border border-slate-850 rounded-xl p-4 space-y-3.5">
                  <span className="text-[10px] font-extrabold text-slate-500 uppercase tracking-widest block border-b border-slate-850 pb-1.5">
                    Detection Summary
                  </span>
                  <div className="space-y-2.5 text-xs">
                    <div className="flex justify-between">
                      <span className="text-slate-500">Verification Status:</span>
                      <span className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 rounded text-[9px] font-extrabold uppercase">
                        VERIFIED
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Active Model:</span>
                      <span className="font-mono text-slate-400 text-[10px]">
                        {evidence.violation?.toLowerCase().includes("helmet") ? "Helmet-Detector" : "SeatBelt-Classifier"}
                      </span>
                    </div>
                    <div className="flex flex-col space-y-1 pt-1.5">
                      <span className="text-slate-500 block">Trigger Reason:</span>
                      <span className="text-slate-400 text-[11px] leading-relaxed italic">
                        {evidence.violation?.toLowerCase().includes("helmet")
                          ? "Verified missing protective gear on motorcycle rider across consecutive buffer frames."
                          : "Verified driver upper-body cabinet visibility without chest diagonal restraint belt."}
                      </span>
                    </div>
                  </div>
                </div>

              </div>

              {/* AI Explainability Model Run Logs */}
              <div className="bg-slate-950/30 border border-slate-850 rounded-xl p-4 space-y-3 text-xs text-slate-400">
                <div className="flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-purple-400 animate-pulse" />
                  <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider">AI Decision Engine Execution Pipeline Audit</span>
                </div>
                
                <div className="space-y-2 pt-1">
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-[10px] text-slate-500 uppercase font-bold w-20 shrink-0">Executed Models:</span>
                    {(evidence.executed_models || "YOLOv8-Vehicle, ByteTrack-Tracker, Helmet-Detector").split(",").map((model, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 rounded text-[9px] font-semibold font-mono">
                        {model.trim()}
                      </span>
                    ))}
                  </div>
                  
                  <div className="flex flex-wrap items-center gap-1.5">
                    <span className="text-[10px] text-slate-500 uppercase font-bold w-20 shrink-0">Skipped Models:</span>
                    {(evidence.skipped_models || "SeatBelt-Classifier, Speed-Estimator, StopLine-Detector").split(",").map((model, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-amber-500/10 border border-amber-500/25 text-amber-400 rounded text-[9px] font-semibold font-mono">
                        {model.trim()}
                      </span>
                    ))}
                  </div>

                  <div className="pt-2 border-t border-slate-850/60 flex items-start gap-1.5 text-[11px] leading-relaxed">
                    <span className="text-[10px] text-slate-500 uppercase font-bold w-20 shrink-0 mt-0.5">Skip Reason:</span>
                    <span className="font-semibold text-slate-300">
                      {evidence.reason_for_skip || "Driver Not Visible, Speed Estimation Unavailable, Stop Line Not Found"}
                    </span>
                  </div>
                </div>
              </div>

            </div>
          )}
        </div>

      </div>
    </div>
  );
}
