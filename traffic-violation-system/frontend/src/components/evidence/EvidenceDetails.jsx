import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Download, Trash2, Calendar, Camera, Info, Tv } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function EvidenceDetails({ activeId, metadata, integrity, onDelete }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('annotated');

  const handleOpenAudit = () => {
    if (!metadata) return;
    const routeMap = {
      "No Helmet": "/helmet-detection",
      "No Seat Belt": "/seatbelt-detection",
      "Distracted Driving": "/mobile-phone",
      "Red Light": "/traffic-light",
      "Speeding": "/speed-detection",
      "Triple Riding": "/triple-riding",
      "Wrong Lane": "/wrong-lane",
      "Stop Line Crossing": "/stop-line",
      "Illegal Parking": "/parking-violation"
    };
    const path = routeMap[metadata.violation || metadata.violation_type];
    if (path) {
      navigate(path, { state: { evidenceList: [metadata] } });
    }
  };

  if (!activeId || !metadata) return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-center text-slate-500 text-xs">
      Select an evidence item from the grid to inspect details.
    </div>
  );

  const isVideo = !!(metadata.video_path || metadata.original_video_path || metadata.annotated_video_path);
  const mediaType = isVideo ? 'video' : 'image';

  // Specific download/preview endpoint mappings
  const originalUrl = `/api/v1/evidence/${activeId}/original?type=${mediaType}`;
  const annotatedUrl = `/api/v1/evidence/${activeId}/processed?type=${mediaType}`;
  const downloadOriginalUrl = evidenceAPI.getDownloadOriginalUrl(activeId);
  const downloadAnnotatedUrl = evidenceAPI.getDownloadAnnotatedUrl(activeId);

  const activeMediaUrl = activeTab === 'original' ? originalUrl : annotatedUrl;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg p-5 space-y-4">
      {/* Title */}
      <div className="flex justify-between items-center text-xs border-b border-slate-850 pb-3">
        <h3 className="font-semibold text-slate-250 uppercase tracking-wider">Inspect Evidence Control</h3>
        <span className="text-[10px] text-purple-400 font-bold bg-slate-950 px-2.5 py-1 rounded border border-slate-850">
          ID: #{activeId}
        </span>
      </div>

      {/* Tabs */}
      <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-850">
        <button
          onClick={() => setActiveTab('original')}
          className={`flex-1 py-1.5 text-[10px] font-bold rounded-md transition-all cursor-pointer ${
            activeTab === 'original'
              ? 'bg-purple-650 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Original Media
        </button>
        <button
          onClick={() => setActiveTab('annotated')}
          className={`flex-1 py-1.5 text-[10px] font-bold rounded-md transition-all cursor-pointer ${
            activeTab === 'annotated'
              ? 'bg-purple-650 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          Annotated Media
        </button>
      </div>

      {/* Preview Canvas */}
      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-955 flex items-center justify-center min-h-[220px]">
        {isVideo ? (
          <video
            key={`${activeId}-${activeTab}`}
            src={activeMediaUrl}
            controls
            className="w-full object-contain max-h-[220px]"
          />
        ) : (
          <img
            key={`${activeId}-${activeTab}`}
            src={activeMediaUrl}
            alt={`preview-${activeId}`}
            className="w-full object-contain max-h-[220px]"
          />
        )}
        <div className="absolute top-2 left-2 bg-slate-950/80 border border-slate-800 text-slate-300 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
          {activeTab === 'original' ? (
            <span>Untouched Original</span>
          ) : (
            <>
              <ShieldCheck className="w-3 h-3 text-emerald-450" />
              <span>AI Annotated</span>
            </>
          )}
        </div>
      </div>

      {/* Metadata grid */}
      <div className="space-y-2">
        <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Metadata Registry</span>
        <div className="bg-slate-955 border border-slate-850 rounded-lg p-3 space-y-2 text-xs font-semibold">
          <div className="flex justify-between">
            <span className="text-slate-500">Violation Category</span>
            <span className="text-slate-250 capitalize">{metadata.violation || 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Vehicle ID</span>
            <span className="text-slate-250 font-mono">#{metadata.vehicle_id || 'N/A'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Plate Number / OCR</span>
            <span className="text-slate-250 font-mono">{metadata.plate_number || 'Not Available'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Confidence Score</span>
            <span className="text-slate-250 font-mono">
              {metadata.confidence ? `${(metadata.confidence * 100).toFixed(0)}%` : '85%'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Camera Source</span>
            <span className="text-slate-250">{metadata.camera_id || 'Upload-Center'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500">Log Timestamp</span>
            <span className="text-slate-250 font-mono">{metadata.timestamp}</span>
          </div>
        </div>
      </div>

      {/* Integrity Verification Check */}
      {integrity && (
        <div className="space-y-2">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">SHA-256 Integrity status</span>
          <div className="bg-slate-955 border border-slate-850 rounded-lg p-3 space-y-2 text-[10px] font-semibold">
            <div className="flex justify-between items-center">
              <span className="text-slate-500">Hash Checksum</span>
              <span className="px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/25 text-emerald-450 rounded text-[9px] font-bold">
                {integrity.status}
              </span>
            </div>
            <p className="text-slate-500 font-mono break-all bg-slate-955 p-2 rounded border border-slate-850/60 leading-normal">
              {integrity.hash}
            </p>
          </div>
        </div>
      )}

      {/* Action buttons */}
      <div className="flex flex-col gap-2 pt-2 border-t border-slate-850">
        <button
          onClick={handleOpenAudit}
          className="w-full py-2 bg-slate-950 border border-slate-850 hover:bg-slate-850 text-slate-200 rounded-xl transition-all cursor-pointer text-xs flex items-center justify-center space-x-2 font-semibold"
        >
          <Tv className="w-3.5 h-3.5 text-purple-400" />
          <span>Open Full Audit Page</span>
        </button>
        <div className="flex gap-2">
          <a
            href={downloadOriginalUrl}
            className="flex-1 bg-slate-955 hover:bg-slate-850 text-slate-200 border border-slate-850 font-semibold py-2 rounded-xl text-[10px] flex items-center justify-center space-x-1 transition-all cursor-pointer text-center"
          >
            <Download className="w-3 h-3 text-slate-400" />
            <span>Download Original</span>
          </a>
          <a
            href={downloadAnnotatedUrl}
            className="flex-1 bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2 rounded-xl text-[10px] flex items-center justify-center space-x-1 transition-all cursor-pointer text-center"
          >
            <Download className="w-3 h-3" />
            <span>Download Annotated</span>
          </a>
        </div>
        <button
          onClick={() => onDelete(activeId)}
          className="w-full py-2 bg-slate-955 border border-slate-850 hover:bg-rose-500/10 text-slate-400 hover:text-rose-500 rounded-xl transition-all cursor-pointer text-xs flex items-center justify-center space-x-2 font-semibold"
          title="Delete log"
        >
          <Trash2 className="w-3.5 h-3.5" />
          <span>Purge Evidence Record</span>
        </button>
      </div>
    </div>
  );
}
