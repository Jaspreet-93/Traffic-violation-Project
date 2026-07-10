import React, { useState, useEffect } from 'react';
import { X, Image, Film, FileText, Download } from 'lucide-react';
import { evidenceAPI } from '../services/api';

export default function EvidenceViewer({ violationId, onClose }) {
  const [evidence, setEvidence] = useState(null);
  const [activeMode, setActiveMode] = useState('image'); // 'image' or 'video'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [useOriginal, setUseOriginal] = useState(true); // Default to original for raw stream preview
  const [mediaError, setMediaError] = useState(false);

  useEffect(() => {
    if (violationId) {
      fetchEvidence();
    }
  }, [violationId]);

  useEffect(() => {
    setMediaError(false);
  }, [useOriginal, activeMode, evidence]);

  const fetchEvidence = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await evidenceAPI.getByViolation(violationId);
      setEvidence(res.data);
      if (res.data && res.data.video_path) {
        setActiveMode('video'); // default to video if available
      } else {
        setActiveMode('image');
      }
    } catch (err) {
      setError(err.response?.data?.detail || "No evidence file records found for this violation ID.");
    } finally {
      setLoading(false);
    }
  };

  const getMediaSrc = () => {
    if (!evidence) return '';
    const mode = useOriginal ? 'original' : 'processed';
    return `/api/v1/evidence/${evidence.evidence_id}/${mode}?type=${activeMode}`;
  };

  if (!violationId) return null;

  return (
    <div className="fixed inset-0 bg-slate-955/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="bg-slate-955 px-6 py-4 border-b border-slate-850 flex items-center justify-between">
          <div>
            <h3 className="font-bold text-lg text-slate-100">Media Evidence Review</h3>
            <span className="text-xs text-slate-500">Record ID: #{violationId}</span>
          </div>
          <div className="flex items-center space-x-3">
            {evidence && (
              <a
                href={getMediaSrc()}
                download
                className="text-slate-350 hover:text-purple-400 p-1.5 rounded-lg border border-slate-800 bg-slate-950/80 flex items-center space-x-1.5 text-[10px] font-bold uppercase transition-all"
                title="Download currently viewed media file"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Media</span>
              </a>
            )}
            <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-850 transition-colors">
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col">
          {loading ? (
            <div className="flex-1 flex items-center justify-center min-h-[300px]">
              <span className="w-8 h-8 rounded-full border-4 border-purple-500 border-t-transparent animate-spin"></span>
            </div>
          ) : error ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-8 min-h-[300px]">
              <FileText className="w-12 h-12 text-slate-700 mb-3" />
              <p className="text-slate-400 font-medium">{error}</p>
              <p className="text-xs text-slate-600 mt-1">If the stream is running, trigger a live violation to create evidence.</p>
            </div>
          ) : (
            <div className="space-y-5 flex-1 flex flex-col justify-between">
              {/* Original vs Annotated toggle */}
              <div className="flex justify-between items-center bg-slate-950/40 p-2.5 rounded-xl border border-slate-850/60">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">
                  Source Stream Mode
                </span>
                <div className="flex items-center bg-slate-950 border border-slate-850 p-1 rounded-lg">
                  <button
                    onClick={() => setUseOriginal(true)}
                    className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase transition-all cursor-pointer ${
                      useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                    }`}
                  >
                    Original
                  </button>
                  <button
                    onClick={() => setUseOriginal(false)}
                    className={`px-3 py-1 rounded-md text-[10px] font-bold uppercase transition-all cursor-pointer ${
                      !useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                    }`}
                  >
                    Annotated AI
                  </button>
                </div>
              </div>

              {/* Media viewer window */}
              <div className="bg-slate-955 border border-slate-850 rounded-xl overflow-hidden flex-1 min-h-[300px] flex items-center justify-center relative">
                {mediaError ? (
                  <div className="text-slate-500 text-xs font-semibold text-center py-12 flex flex-col items-center justify-center space-y-2">
                    <FileText className="w-10 h-10 text-slate-700" />
                    <span>Evidence file not available.</span>
                  </div>
                ) : activeMode === 'image' ? (
                  <img
                    key={useOriginal ? 'orig-img' : 'ann-img'}
                    src={getMediaSrc()}
                    alt="Infraction snapshot"
                    className="w-full h-full object-contain max-h-[400px]"
                    onError={() => setMediaError(true)}
                  />
                ) : (
                  <video
                    key={useOriginal ? 'orig-vid' : 'ann-vid'}
                    src={getMediaSrc()}
                    controls
                    autoPlay
                    className="w-full h-full object-contain max-h-[400px]"
                    onError={() => setMediaError(true)}
                  />
                )}
              </div>

              {/* Options panel */}
              <div className="grid grid-cols-2 gap-4">
                <button
                  onClick={() => setActiveMode('image')}
                  className={`flex items-center justify-center space-x-2 py-3 rounded-xl border text-sm font-semibold transition-all cursor-pointer ${
                    activeMode === 'image'
                      ? 'bg-purple-650/10 border-purple-500 text-purple-400'
                      : 'border-slate-800 bg-slate-950/40 hover:bg-slate-850 text-slate-400'
                  }`}
                >
                  <Image className="w-4 h-4" />
                  <span>Snapshot Image</span>
                </button>
                <button
                  onClick={() => setActiveMode('video')}
                  className={`flex items-center justify-center space-x-2 py-3 rounded-xl border text-sm font-semibold transition-all cursor-pointer ${
                    activeMode === 'video'
                      ? 'bg-purple-650/10 border-purple-500 text-purple-400'
                      : 'border-slate-800 bg-slate-950/40 hover:bg-slate-850 text-slate-400'
                  }`}
                >
                  <Film className="w-4 h-4" />
                  <span>Video Clip</span>
                </button>
              </div>

              {/* Meta details list */}
              <div className="bg-slate-955/50 border border-slate-850 rounded-xl p-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-xs text-slate-400">
                <div>
                  <span className="text-slate-500 block uppercase font-bold tracking-wider text-[10px]">Vehicle ID</span>
                  <span className="font-semibold text-slate-350">{evidence.vehicle_id || '99'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-bold tracking-wider text-[10px]">Plate Number</span>
                  <span className="font-semibold text-slate-350">{evidence.plate_number || 'PB10AB1234'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-bold tracking-wider text-[10px]">Violation Type</span>
                  <span className="font-semibold text-slate-350">{evidence.violation || 'No Helmet'}</span>
                </div>
                <div>
                  <span className="text-slate-500 block uppercase font-bold tracking-wider text-[10px]">Capture Time</span>
                  <span className="font-semibold text-slate-350">{evidence.timestamp}</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
