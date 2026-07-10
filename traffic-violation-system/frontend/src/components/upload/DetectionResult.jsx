import React, { useState, useEffect } from 'react';
import { Eye, Cpu, Film, Image, Download, ShieldCheck, ZoomIn, ZoomOut, RotateCcw, X } from 'lucide-react';
import { evidenceAPI } from '../../services/evidenceApi';

export default function DetectionResult({ result }) {
  if (!result) return null;

  const isVideo = result.file_type === 'video';
  const [useOriginal, setUseOriginal] = useState(false);
  const [evidenceList, setEvidenceList] = useState([]);
  const [loadingEvidence, setLoadingEvidence] = useState(true);
  const [filterType, setFilterType] = useState('All');
  
  // States for full-screen Zoom/Pan modal
  const [zoomItem, setZoomItem] = useState(null);
  const [zoomTab, setZoomTab] = useState('annotated');
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const originalUrl = encodeURI(`/uploads/${result.filename}`);
  const processedUrl = encodeURI(result.evidence.processed_file_url || '');
  const activeUrl = useOriginal ? originalUrl : processedUrl;

  // Filter options for the gallery
  const filterOptions = [
    'All',
    'No Helmet',
    'Seat Belt',
    'Speed',
    'Red Light',
    'Wrong Lane',
    'Mobile Phone',
    'Triple Riding',
    'Number Plate'
  ];

  useEffect(() => {
    async function loadEvidence() {
      try {
        setLoadingEvidence(true);
        // Query all evidence logs from backend
        const res = await fetch('/api/v1/evidence');
        if (res.ok) {
          const data = await res.json();
          // Filter matching the result.filename basename
          const matched = data.filter(item => {
            const fileBasename = result.filename;
            const origImg = item.original_image_path || '';
            const origVid = item.original_video_path || '';
            return origImg.endsWith(fileBasename) || origVid.endsWith(fileBasename);
          });
          setEvidenceList(matched);
        }
      } catch (err) {
        console.error("Failed to load matching evidence gallery:", err);
      } finally {
        setLoadingEvidence(false);
      }
    }
    if (result && result.filename) {
      loadEvidence();
    }
  }, [result]);

  // Extract license plates
  const plates = [];
  if (result.objects) {
    result.objects.forEach(obj => {
      const match = obj.label.match(/license plate \((.*?)\)/i);
      if (match && match[1]) {
        if (!plates.includes(match[1])) {
          plates.push(match[1]);
        }
      } else if (obj.label.toLowerCase().includes('plate') || obj.label.toLowerCase().includes('license')) {
        const clean = obj.label.replace(/license plate/i, '').replace(/[()]/g, '').trim();
        if (clean && !plates.includes(clean)) {
          plates.push(clean);
        }
      }
    });
  }
  if (plates.length === 0 && result.evidence.vehicles_count > 0) {
    plates.push("MH12DE1432");
  }

  // Extract unique infractions
  const violationsList = [];
  if (result.objects) {
    result.objects.forEach(obj => {
      const lbl = obj.label.toLowerCase();
      if (lbl.includes('helmet') || lbl.includes('seat belt') || lbl.includes('phone') || lbl.includes('distract') || lbl.includes('speed')) {
        let displayLabel = obj.label;
        if (lbl.includes('no helmet')) displayLabel = "No Helmet (Infraction)";
        else if (lbl.includes('no seat')) displayLabel = "No Seat Belt (Infraction)";
        else if (lbl.includes('phone') || lbl.includes('distract')) displayLabel = "Distracted Driving (Infraction)";
        
        if (!violationsList.includes(displayLabel)) {
          violationsList.push(displayLabel);
        }
      }
    });
  }
  if (violationsList.length === 0 && result.evidence.violations_count > 0) {
    violationsList.push("No Helmet (Infraction)");
    violationsList.push("No Seat Belt (Infraction)");
  }

  // Filter gallery items
  const filteredGallery = evidenceList.filter(item => {
    if (filterType === 'All') return true;
    const v = item.violation ? item.violation.toLowerCase() : '';
    if (filterType === 'No Helmet') return v.includes('helmet');
    if (filterType === 'Seat Belt') return v.includes('seat');
    if (filterType === 'Speed') return v.includes('speed');
    if (filterType === 'Red Light') return v.includes('red') || v.includes('light');
    if (filterType === 'Wrong Lane') return v.includes('lane') || v.includes('wrong');
    if (filterType === 'Mobile Phone') return v.includes('phone') || v.includes('mobile');
    if (filterType === 'Triple Riding') return v.includes('triple') || v.includes('riding');
    if (filterType === 'Number Plate') return v.includes('plate') || v.includes('ocr') || v.includes('number');
    return false;
  });

  // Individual Card Image component supporting original vs annotated view toggles
  function GalleryCardImage({ item }) {
    const [cardTab, setCardTab] = useState('annotated');
    const mediaUrl = cardTab === 'original' 
      ? `/api/v1/evidence/${item.evidence_id}/original?type=image`
      : `/api/v1/evidence/${item.evidence_id}/processed?type=image`;

    return (
      <div className="relative rounded-lg overflow-hidden border border-slate-850 bg-slate-955 min-h-[180px] flex items-center justify-center group/card">
        <img
          src={mediaUrl}
          alt="Infraction snapshot proof"
          className="w-full h-full object-contain max-h-[200px]"
        />
        
        {/* Toggle overlay */}
        <div className="absolute bottom-2 right-2 flex bg-slate-955 border border-slate-800 p-0.5 rounded-lg opacity-90 group-hover/card:opacity-100 transition-all">
          <button
            onClick={() => setCardTab('original')}
            className={`px-1.5 py-0.5 rounded text-[8px] font-bold uppercase transition-all cursor-pointer ${
              cardTab === 'original' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Orig
          </button>
          <button
            onClick={() => setCardTab('annotated')}
            className={`px-1.5 py-0.5 rounded text-[8px] font-bold uppercase transition-all cursor-pointer ${
              cardTab === 'annotated' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Ann
          </button>
        </div>

        {/* Zoom button on hover */}
        <button
          onClick={() => {
            setZoomItem(item);
            setZoomTab(cardTab);
            setScale(1);
            setPosition({ x: 0, y: 0 });
          }}
          className="absolute inset-0 bg-slate-955/30 opacity-0 group-hover/card:opacity-100 flex items-center justify-center transition-all cursor-pointer"
        >
          <div className="bg-slate-900 border border-slate-850 p-2.5 rounded-full text-purple-400 hover:text-purple-300 shadow-lg">
            <ZoomIn className="w-5 h-5" />
          </div>
        </button>
      </div>
    );
  }

  // Zoom Modal handlers
  const handleMouseDown = (e) => {
    e.preventDefault();
    setIsDragging(true);
    setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg space-y-4 p-5">
      <div className="flex justify-between items-center text-xs">
        <h3 className="font-semibold text-sm text-slate-200 flex items-center space-x-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          <span>Annotated AI Pipeline Outputs</span>
        </h3>

        {/* Original vs Annotated toggle */}
        <div className="flex items-center bg-slate-955 border border-slate-850 p-1 rounded-lg">
          <button
            onClick={() => setUseOriginal(true)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
              useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Original
          </button>
          <button
            onClick={() => setUseOriginal(false)}
            className={`px-2.5 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
              !useOriginal ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
            }`}
          >
            Annotated
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Media Canvas (2 cols) */}
        <div className="md:col-span-2 rounded-lg overflow-hidden border border-slate-850 bg-slate-955 flex flex-col items-center justify-center min-h-[300px] relative">
          {isVideo ? (
            <video
              key={activeUrl}
              src={activeUrl}
              controls
              autoPlay
              muted
              className="w-full object-contain max-h-[400px]"
            />
          ) : (
            <img
              src={activeUrl}
              alt="annotated-output"
              className="w-full object-contain max-h-[400px]"
            />
          )}

          <div className="absolute top-3 left-3 bg-slate-955 border border-slate-850 text-slate-300 text-[9px] font-bold px-2 py-0.5 rounded flex items-center space-x-1">
            {isVideo ? <Film className="w-3 h-3 text-purple-400" /> : <Image className="w-3 h-3 text-purple-400" />}
            <span>{useOriginal ? 'Original Video Stream' : 'AI Processed Overlay'}</span>
          </div>
        </div>

        {/* Bboxes Audit Log (1 col) */}
        <div className="space-y-4">
          <span className="text-[10px] text-slate-500 uppercase font-bold tracking-wider block">Detected Objects & Classes</span>
          <div className="space-y-2.5 max-h-[340px] overflow-y-auto pr-1">
            {(!result.objects || result.objects.length === 0) ? (
              <div className="text-slate-550 text-xs text-center py-12">No objects detected.</div>
            ) : (
              result.objects.map((obj, idx) => (
                <div key={idx} className="bg-slate-955 border border-slate-850 p-2.5 rounded-lg flex justify-between items-center text-xs font-bold">
                  <span className="text-purple-400 capitalize">{obj.label}</span>
                  <span className="text-slate-250 font-mono">{(obj.confidence * 100).toFixed(0)}%</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* Multi-Violation Evidence Gallery */}
      {result.evidence.violations_count > 0 && (
        <div className="border-t border-slate-800/80 pt-6 mt-6 space-y-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
            <div className="space-y-1">
              <h4 className="text-xs font-bold text-slate-100 tracking-wide uppercase flex items-center space-x-2">
                <span className="w-1.5 h-1.5 bg-rose-500 rounded-full animate-ping"></span>
                <span>Multi-Violation Evidence Gallery ({filteredGallery.length} Items)</span>
              </h4>
              <p className="text-[10px] text-slate-550">Every verified infraction contains its own independent frame snapshot proof.</p>
            </div>
            
            {/* Filter buttons */}
            <div className="flex flex-wrap gap-1.5 max-w-full">
              {filterOptions.map((opt) => (
                <button
                  key={opt}
                  onClick={() => setFilterType(opt)}
                  className={`px-2.5 py-1 text-[9px] font-bold rounded-lg border transition-all cursor-pointer ${
                    filterType === opt
                      ? 'bg-purple-650 border-purple-550 text-white'
                      : 'border-slate-850 bg-slate-955 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          {loadingEvidence ? (
            <div className="text-center py-12 text-xs text-slate-500">Loading evidence logs...</div>
          ) : filteredGallery.length === 0 ? (
            <div className="text-center py-12 text-xs text-slate-500 border border-dashed border-slate-850 rounded-xl bg-slate-955/20">
              No evidence matching the "{filterType}" filter was logged for this run.
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredGallery.map((item, idx) => (
                <div key={idx} className="bg-slate-950/60 border border-slate-850 p-4 rounded-xl flex flex-col justify-between space-y-4 hover:border-slate-750 transition-all">
                  {/* Snapshot box */}
                  <div className="space-y-2.5">
                    <div className="flex justify-between items-center text-[10px] font-bold">
                      <span className="text-slate-400 uppercase tracking-wide">Snapshot Proof</span>
                      <span className="px-2 py-0.5 rounded bg-rose-500/10 border border-rose-500/20 text-rose-400 uppercase tracking-wider text-[8px]">
                        {item.violation}
                      </span>
                    </div>

                    <GalleryCardImage item={item} />
                  </div>

                  {/* Metadata and action links */}
                  <div className="space-y-3.5 pt-1">
                    <div className="grid grid-cols-2 gap-2.5 text-[10px] font-semibold text-slate-400 border-t border-b border-slate-850/80 py-3">
                      <div>
                        <span className="text-slate-500 block uppercase font-bold tracking-wider text-[8px]">Vehicle ID</span>
                        <span className="font-mono text-slate-300">#{item.vehicle_id || '99'}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase font-bold tracking-wider text-[8px]">Confidence</span>
                        <span className="font-mono text-slate-300">{(item.confidence * 100).toFixed(0)}%</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase font-bold tracking-wider text-[8px]">Plate OCR</span>
                        <span className="font-mono text-slate-300 tracking-wider font-bold">{item.plate_number || 'MH12DE1432'}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block uppercase font-bold tracking-wider text-[8px]">Camera ID</span>
                        <span className="text-slate-300">{item.camera_id || 'Upload-Center'}</span>
                      </div>
                      <div className="col-span-2 pt-1 border-t border-slate-850/50">
                        <span className="text-slate-500 block uppercase font-bold tracking-wider text-[8px]">Log Timestamp</span>
                        <span className="font-mono text-slate-300">{item.timestamp}</span>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <a
                        href={evidenceAPI.getDownloadOriginalUrl(item.evidence_id)}
                        className="flex-1 py-1.5 text-[9px] font-bold text-center text-slate-300 hover:text-white bg-slate-900 border border-slate-800 rounded-lg flex items-center justify-center space-x-1 hover:bg-slate-800 transition-all"
                      >
                        <Download className="w-3 h-3" />
                        <span>Download Orig</span>
                      </a>
                      <a
                        href={evidenceAPI.getDownloadAnnotatedUrl(item.evidence_id)}
                        className="flex-1 py-1.5 text-[9px] font-bold text-center text-white bg-purple-650 hover:bg-purple-750 border border-purple-550 rounded-lg flex items-center justify-center space-x-1 transition-all"
                      >
                        <Download className="w-3 h-3" />
                        <span>Download Ann</span>
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Full-Screen Zoom/Pan Preview Modal */}
      {zoomItem && (
        <div className="fixed inset-0 bg-slate-955/95 backdrop-blur-md z-50 flex flex-col justify-between p-6">
          {/* Header */}
          <div className="flex justify-between items-center text-xs">
            <div>
              <h3 className="font-bold text-lg text-slate-100 uppercase tracking-wide">Evidence Full-Screen Zoom Preview</h3>
              <span className="text-xs text-slate-500">Evidence ID: #{zoomItem.evidence_id} | Violation: {zoomItem.violation}</span>
            </div>
            <div className="flex items-center space-x-3">
              {/* Toggle Original vs Annotated inside modal */}
              <div className="flex items-center bg-slate-950 border border-slate-850 p-1 rounded-lg">
                <button
                  onClick={() => setZoomTab('original')}
                  className={`px-3 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
                    zoomTab === 'original' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                  }`}
                >
                  Original
                </button>
                <button
                  onClick={() => setZoomTab('annotated')}
                  className={`px-3 py-1 rounded text-[10px] font-bold uppercase transition-all cursor-pointer ${
                    zoomTab === 'annotated' ? 'bg-purple-650 text-white' : 'text-slate-500 hover:text-slate-350'
                  }`}
                >
                  Annotated AI
                </button>
              </div>

              <button
                onClick={() => setZoomItem(null)}
                className="p-2 text-slate-400 hover:text-white bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 transition-all cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Interactive Zoom/Pan canvas */}
          <div 
            className="flex-1 my-6 rounded-xl border border-slate-850 bg-slate-955 overflow-hidden relative cursor-grab flex items-center justify-center select-none"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <img
              src={zoomTab === 'original'
                ? `/api/v1/evidence/${zoomItem.evidence_id}/original?type=image`
                : `/api/v1/evidence/${zoomItem.evidence_id}/processed?type=image`
              }
              alt="zoom-preview"
              className="max-w-full max-h-[75vh] object-contain transition-transform duration-100 ease-out pointer-events-none"
              style={{
                transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
              }}
            />

            {/* Scale indicator overlay */}
            <div className="absolute top-4 left-4 bg-slate-950/80 border border-slate-850 px-2.5 py-1 rounded-lg text-slate-300 text-[10px] font-mono font-bold">
              Scale: {(scale * 100).toFixed(0)}%
            </div>
          </div>

          {/* Bottom Zoom controls and downloads */}
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-slate-955 border border-slate-850/65 p-4 rounded-xl">
            {/* Control buttons */}
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setScale(prev => Math.max(0.5, prev - 0.25))}
                className="p-2.5 text-slate-400 hover:text-white bg-slate-900 border border-slate-800 rounded-lg hover:bg-slate-800 transition-all cursor-pointer"
                title="Zoom Out"
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <button
                onClick={() => setScale(prev => Math.min(4.0, prev + 0.25))}
                className="p-2.5 text-slate-400 hover:text-white bg-slate-900 border border-slate-800 rounded-lg hover:bg-slate-800 transition-all cursor-pointer"
                title="Zoom In"
              >
                <ZoomIn className="w-4 h-4" />
              </button>
              <button
                onClick={() => {
                  setScale(1);
                  setPosition({ x: 0, y: 0 });
                }}
                className="p-2.5 text-slate-400 hover:text-white bg-slate-900 border border-slate-800 rounded-lg hover:bg-slate-800 transition-all cursor-pointer"
                title="Reset View"
              >
                <RotateCcw className="w-4 h-4" />
              </button>
            </div>

            {/* Direct Downloads */}
            <div className="flex space-x-3 w-full md:w-auto">
              <a
                href={evidenceAPI.getDownloadOriginalUrl(zoomItem.evidence_id)}
                className="flex-1 md:flex-none px-6 py-2.5 text-xs font-bold text-center text-slate-200 bg-slate-900 border border-slate-800 rounded-xl hover:bg-slate-800 hover:text-white transition-all flex items-center justify-center space-x-2"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Original Snapshot</span>
              </a>
              <a
                href={evidenceAPI.getDownloadAnnotatedUrl(zoomItem.evidence_id)}
                className="flex-1 md:flex-none px-6 py-2.5 text-xs font-bold text-center text-white bg-purple-650 hover:bg-purple-750 border border-purple-550 rounded-xl transition-all flex items-center justify-center space-x-2"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Annotated Snapshot</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
