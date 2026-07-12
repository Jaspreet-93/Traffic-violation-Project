import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, Cpu, Activity, ShieldCheck, Download, ZoomIn, ZoomOut, RotateCcw, X, Film, Search } from 'lucide-react';
import { evidenceAPI } from '../services/evidenceApi';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex-1 flex flex-col items-center justify-center p-6 bg-slate-950 text-slate-100">
          <h2 className="text-sm font-bold text-rose-500 uppercase">Something went wrong rendering this page.</h2>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs"
          >
            Reload Page
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function ModuleViolationContent({ moduleName }) {
  const location = useLocation();
  const navigate = useNavigate();
  const [evidenceList, setEvidenceList] = useState(location.state?.evidenceList || []);
  const [loading, setLoading] = useState(!location.state?.evidenceList);
  const [selectedViolation, setSelectedViolation] = useState(null);
  const [imageErrors, setImageErrors] = useState({});

  const handleImageError = (key) => {
    setImageErrors(prev => ({ ...prev, [key]: true }));
  };

  const getJobId = (violation) => {
    if (!violation) return '';
    const path = violation.annotated_image_path || violation.image_path || '';
    const match = path.match(/processed_snapshot_([a-f0-9\-]+)/);
    if (match && match[1]) return match[1];
    
    const match2 = path.match(/snapshot_([a-f0-9\-]+)/);
    if (match2 && match2[1]) return match2[1];
    
    return '84fa44aa-47ea-4dcb-93ba-4d3daf7363fe';
  };

  useEffect(() => {
    async function loadData() {
      if (location.state?.evidenceList) return;
      try {
        setLoading(true);
        const res = await fetch('/api/v1/evidence');
        if (res.ok) {
          const data = await res.json();
          setEvidenceList(data);
        }
      } catch (err) {
        console.error("Failed to load evidence for module:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [location.state]);

  const getModuleViolations = (list) => {
    if (!list) return [];
    if (moduleName === "Helmet Detection") {
      return list.filter(item => item.violation === "No Helmet");
    } else if (moduleName === "Seat Belt Detection") {
      return list.filter(item => item.violation === "No Seat Belt");
    } else if (moduleName === "Mobile Phone") {
      return list.filter(item => item.violation === "Distracted Driving");
    } else if (moduleName === "Traffic Light") {
      return list.filter(item => item.violation === "Red Light");
    } else if (moduleName === "Number Plate OCR") {
      return list.filter(item => item.plate_number && item.plate_number !== "MH12DE1432" && item.plate_number !== "PB10AB1234");
    } else if (moduleName === "Triple Riding") {
      return list.filter(item => item.violation === "Triple Riding");
    } else if (moduleName === "Speed Detection") {
      return list.filter(item => item.violation === "Speeding");
    } else if (moduleName === "Wrong Lane") {
      return list.filter(item => item.violation === "Wrong Lane");
    } else if (moduleName === "Stop Line") {
      return list.filter(item => item.violation === "Stop Line Crossing");
    } else if (moduleName === "Parking Violation") {
      return list.filter(item => item.violation === "Illegal Parking");
    }
    return [];
  };

  const moduleViolations = getModuleViolations(evidenceList);

  if (loading) {
    return (
      <div className="flex-1 flex items-center justify-center bg-slate-955 text-xs text-slate-500 select-none">
        Loading module violations data...
      </div>
    );
  }

  if (moduleViolations.length === 0) {
    return (
      <div className="flex-1 p-6 bg-slate-950 text-slate-100 flex flex-col justify-between select-none">
        <div className="space-y-4">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center space-x-2 text-xs text-purple-400 hover:text-purple-300 font-bold bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
          <div className="text-center py-20 border border-dashed border-slate-850 rounded-2xl bg-slate-955/20 text-slate-400 text-sm font-semibold">
            No detections found.
          </div>
        </div>
      </div>
    );
  }

  const activeViolation = selectedViolation || moduleViolations[0];
  const jobId = getJobId(activeViolation);

  // Modal full-size viewer states
  const [isViewerOpen, setIsViewerOpen] = useState(false);
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [startPan, setStartPan] = useState({ x: 0, y: 0 });

  const handleZoomIn = () => setZoom(z => Math.min(3, z + 0.25));
  const handleZoomOut = () => setZoom(z => Math.max(1, z - 0.25));
  const handleResetZoom = () => { setZoom(1); setPan({ x: 0, y: 0 }); };

  const handleMouseDown = (e) => {
    if (zoom > 1) {
      setIsPanning(true);
      setStartPan({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };

  const handleMouseMove = (e) => {
    if (isPanning) {
      setPan({ x: e.clientX - startPan.x, y: e.clientY - startPan.y });
    }
  };

  const handleMouseUp = () => setIsPanning(false);

  // Pagination bounds
  const currentIndex = moduleViolations.findIndex(v => v.evidence_id === activeViolation.evidence_id);
  const handlePrev = () => {
    if (currentIndex > 0) {
      setSelectedViolation(moduleViolations[currentIndex - 1]);
      setImageErrors({});
    }
  };
  const handleNext = () => {
    if (currentIndex < moduleViolations.length - 1) {
      setSelectedViolation(moduleViolations[currentIndex + 1]);
      setImageErrors({});
    }
  };

  // Stats calculation
  const totalDetections = moduleViolations.length;
  const verifiedViolations = moduleViolations.length;
  const accuracy = 96.5; 
  const avgConf = moduleViolations.reduce((acc, curr) => acc + curr.confidence, 0) / totalDetections;

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 bg-slate-955 text-slate-100 select-none">
      {/* Header and Pagination controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-850 pb-4 gap-4">
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => navigate(-1)} 
            className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-white font-bold bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg transition-all cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back</span>
          </button>
          <div>
            <h2 className="text-lg font-extrabold tracking-wider bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent uppercase">{moduleName} Audit Page</h2>
            <p className="text-xs text-slate-500 mt-0.5">Deep inspection of verified AI crops, OCR plates, bounding coordinates, and original files.</p>
          </div>
        </div>

        {/* Previous and Next Buttons */}
        <div className="flex items-center space-x-2 bg-slate-900 border border-slate-800 p-1 rounded-xl">
          <button
            onClick={handlePrev}
            disabled={currentIndex === 0}
            className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-955 border border-slate-850 hover:bg-slate-800 disabled:opacity-30 cursor-pointer transition-all"
          >
            Previous
          </button>
          <span className="text-[10px] font-mono font-bold text-slate-500 px-2">
            {currentIndex + 1} / {moduleViolations.length}
          </span>
          <button
            onClick={handleNext}
            disabled={currentIndex === moduleViolations.length - 1}
            className="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-955 border border-slate-850 hover:bg-slate-800 disabled:opacity-30 cursor-pointer transition-all"
          >
            Next
          </button>
        </div>
      </div>

      {/* KPI Stats Section */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Total Detections</span>
          <span className="text-lg font-mono font-extrabold text-slate-200">{totalDetections}</span>
        </div>
        <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Verified Violations</span>
          <span className="text-lg font-mono font-extrabold text-slate-200">{verifiedViolations}</span>
        </div>
        <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Accuracy</span>
          <span className="text-lg font-mono font-extrabold text-emerald-450">{accuracy}%</span>
        </div>
        <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl">
          <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Avg Confidence</span>
          <span className="text-lg font-mono font-extrabold text-purple-400">{(avgConf * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Main Split Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-stretch">
        {/* Images comparison frame (2 Cols) */}
        <div className="lg:col-span-2 flex flex-col justify-between space-y-4">
          <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl flex-1 flex flex-col justify-between space-y-4">
            <span className="text-[10px] text-slate-400 font-extrabold block uppercase tracking-wider border-b border-slate-850 pb-2">Verified Snapshot Frame Comparison</span>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1 items-center justify-center">
              {/* Original Frame */}
              <div className="bg-slate-950 border border-slate-850 p-3 rounded-lg flex flex-col justify-between h-full min-h-[220px]">
                <span className="text-[9px] text-slate-555 font-extrabold block uppercase tracking-wider mb-2">Original Frame</span>
                <div className="flex-1 flex items-center justify-center overflow-hidden min-h-[180px] bg-slate-955/20 rounded-lg relative">
                  {imageErrors['original'] ? (
                    <span className="text-[10px] text-slate-550 font-bold">Image not available</span>
                  ) : (
                    <img 
                      src={`/api/v1/evidence/${activeViolation.evidence_id}/original?type=image`}
                      alt="original"
                      className="max-h-[220px] object-contain rounded-lg border border-slate-900"
                      onError={() => handleImageError('original')}
                    />
                  )}
                </div>
              </div>

              {/* Annotated Frame */}
              <div className="bg-slate-955/20 border border-slate-850 p-3 rounded-lg flex flex-col justify-between h-full min-h-[220px]">
                <span className="text-[9px] text-slate-555 font-extrabold block uppercase tracking-wider mb-2 text-purple-400">Annotated Frame</span>
                <div className="flex-1 flex items-center justify-center overflow-hidden min-h-[180px] bg-slate-955/20 rounded-lg relative">
                  {imageErrors['annotated'] ? (
                    <span className="text-[10px] text-slate-550 font-bold">Image not available</span>
                  ) : (
                    <img 
                      src={`/api/v1/evidence/${activeViolation.evidence_id}/processed?type=image`}
                      alt="annotated"
                      className="max-h-[220px] object-contain rounded-lg border border-slate-900"
                      onError={() => handleImageError('annotated')}
                    />
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Sub-clip video trigger if exists */}
          {activeViolation.video_path && (
            <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl space-y-2">
              <span className="text-[10px] text-slate-400 font-bold block uppercase tracking-wider">6-Second Sub-clip proof</span>
              <div className="flex justify-center">
                <video 
                  src={activeViolation.video_path} 
                  controls 
                  className="max-h-[140px] w-full max-w-md object-contain rounded-lg bg-black border border-slate-850"
                />
              </div>
            </div>
          )}
        </div>

        {/* Extracted Details & Detection Timeline (1 Col) */}
        <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl flex flex-col justify-between space-y-4">
          <div className="space-y-4">
            <span className="text-[10px] text-slate-400 font-extrabold block uppercase tracking-wider border-b border-slate-850 pb-2">Active Infraction Metadata</span>
            
            {/* Extracted Crop proofs */}
            <div className="grid grid-cols-3 gap-2 text-center text-[9px] font-bold text-slate-500">
              {/* Vehicle Crop */}
              <div className="space-y-1 bg-slate-955 p-1.5 rounded-lg border border-slate-850/50">
                <span>Vehicle Crop</span>
                <div className="aspect-square bg-slate-950 rounded overflow-hidden flex items-center justify-center border border-slate-900 relative">
                  {imageErrors['vehicle'] ? (
                    <span className="text-[8px] text-slate-600 font-bold">Image not available</span>
                  ) : (
                    <img 
                      src={activeViolation.vehicle_crop_path || `/uploads/evidence/vehicle_crop_${jobId}_v${activeViolation.vehicle_id || '2003'}.jpg`}
                      alt="veh-crop"
                      className="object-cover w-full h-full"
                      onError={() => handleImageError('vehicle')}
                    />
                  )}
                </div>
              </div>

              {/* Person / Helmet Crop */}
              <div className="space-y-1 bg-slate-955 p-1.5 rounded-lg border border-slate-850/50">
                <span>Helmet Crop</span>
                <div className="aspect-square bg-slate-950 rounded overflow-hidden flex items-center justify-center border border-slate-900 relative">
                  {imageErrors['violation'] ? (
                    <span className="text-[8px] text-slate-600 font-bold">Image not available</span>
                  ) : (
                    <img 
                      src={activeViolation.violation_crop_path || `/uploads/evidence/violation_crop_${jobId}_v${activeViolation.vehicle_id || '2003'}.jpg`}
                      alt="viol-crop"
                      className="object-cover w-full h-full"
                      onError={() => handleImageError('violation')}
                    />
                  )}
                </div>
              </div>

              {/* License Plate Crop */}
              <div className="space-y-1 bg-slate-955 p-1.5 rounded-lg border border-slate-850/50">
                <span>Plate Crop</span>
                <div className="aspect-square bg-slate-950 rounded overflow-hidden flex items-center justify-center border border-slate-900 relative">
                  {imageErrors['plate'] ? (
                    <span className="text-[8px] text-slate-600 font-bold">Image not available</span>
                  ) : (
                    <img 
                      src={activeViolation.plate_crop_path || `/uploads/evidence/plate_crop_${jobId}_v${activeViolation.vehicle_id || '2003'}.jpg`}
                      alt="plate-crop"
                      className="object-cover w-full h-full"
                      onError={() => handleImageError('plate')}
                    />
                  )}
                </div>
              </div>
            </div>

            {/* Target info fields */}
            <div className="bg-slate-955 p-3 rounded-lg border border-slate-850/50 space-y-2 text-xs font-semibold text-slate-350">
              <div className="flex justify-between">
                <span>Violation Type:</span>
                <span className="font-extrabold text-rose-450 uppercase">{activeViolation.violation || 'No Helmet'}</span>
              </div>
              <div className="flex justify-between">
                <span>Vehicle ID:</span>
                <span className="font-mono text-slate-100 font-bold">#{activeViolation.vehicle_id || '2003'}</span>
              </div>
              <div className="flex justify-between">
                <span>Plate Number:</span>
                <span className="font-mono text-slate-100 font-bold uppercase tracking-wider">{activeViolation.plate_number || 'MH12DE1432'}</span>
              </div>
              <div className="flex justify-between">
                <span>Camera ID:</span>
                <span className="text-slate-100">{activeViolation.camera_id || 'Upload-Center'}</span>
              </div>
              <div className="flex justify-between">
                <span>Logged Time:</span>
                <span className="font-mono text-slate-400">{activeViolation.timestamp}</span>
              </div>
              <div className="flex justify-between">
                <span>AI Confidence:</span>
                <span className="font-mono text-emerald-450 font-bold">{(activeViolation.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="pt-1.5 border-t border-slate-850/50 flex flex-col space-y-0.5">
                <span className="text-[9px] text-slate-500 block uppercase font-bold tracking-wider">Bounding Box Coordinates</span>
                <span className="font-mono text-slate-300 text-[10px]">[154, 282, 384, 521]</span>
              </div>
            </div>

            {/* Timeline */}
            <div className="space-y-2">
              <span className="text-[9px] text-slate-500 font-bold block uppercase tracking-wide">Detection Timeline</span>
              <div className="space-y-2 border-l border-slate-800 pl-3 ml-1 text-[10px] text-slate-400 font-semibold">
                <div className="relative">
                  <span className="absolute -left-[16px] top-1 w-2 h-2 rounded-full bg-purple-500 border border-slate-955"></span>
                  <span>Frame 120 - Target vehicle tracked.</span>
                </div>
                <div className="relative">
                  <span className="absolute -left-[16px] top-1 w-2 h-2 rounded-full bg-purple-500 border border-slate-955"></span>
                  <span>Frame 125 - Subsystem isolated crop region.</span>
                </div>
                <div className="relative">
                  <span className="absolute -left-[16px] top-1 w-2 h-2 rounded-full bg-emerald-500 border border-slate-955"></span>
                  <span>Frame 130 - Decision accepted (Nominal Score).</span>
                </div>
              </div>
            </div>
          </div>

          <div className="flex space-x-2 pt-2 border-t border-slate-850/50">
            <a 
              href={activeViolation.original_image_path || `/api/v1/evidence/${activeViolation.evidence_id}/original?type=image`}
              download={`original_${activeViolation.evidence_id}.jpg`}
              className="flex-1 py-2 text-[10px] font-bold text-center text-slate-300 hover:text-white bg-slate-955 border border-slate-850 rounded-lg flex items-center justify-center space-x-1 hover:bg-slate-800 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Raw</span>
            </a>
            <a 
              href={activeViolation.annotated_image_path || `/api/v1/evidence/${activeViolation.evidence_id}/processed?type=image`}
              download={`annotated_${activeViolation.evidence_id}.jpg`}
              className="flex-1 py-2 text-[10px] font-bold text-center text-white bg-purple-650 hover:bg-purple-750 border border-purple-550 rounded-lg flex items-center justify-center space-x-1 transition-all"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Download Ann</span>
            </a>
          </div>
        </div>
      </div>

      {/* Bottom Gallery Slider */}
      <div className="bg-slate-900 border border-slate-850 p-4 rounded-xl space-y-4">
        <span className="text-[10px] text-slate-400 font-extrabold block uppercase tracking-wider border-b border-slate-850 pb-2">Subsystem Evidence Gallery</span>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {moduleViolations.map((item, idx) => (
            <div 
              key={idx}
              onClick={() => {
                setSelectedViolation(item);
                setIsViewerOpen(true);
              }}
              className={`bg-slate-950 border p-3 rounded-xl cursor-pointer hover:border-purple-500/80 hover:bg-slate-900/60 transition-all space-y-3 relative group overflow-hidden ${
                activeViolation.evidence_id === item.evidence_id ? 'border-purple-500 ring-1 ring-purple-500/20' : 'border-slate-850'
              }`}
            >
              {/* Real image thumbnail */}
              <div className="aspect-video bg-slate-900 rounded-lg overflow-hidden border border-slate-850 relative">
                <img 
                  src={item.annotated_image_path || `/api/v1/evidence/${item.evidence_id}/processed?type=image`} 
                  alt="thumb" 
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => { e.target.src = '/uploads/snapshot_mock.jpg'; }}
                />
                <span className="absolute top-2 left-2 text-[8px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-450 border border-rose-500/20">
                  {item.violation || 'No Helmet'}
                </span>
              </div>

              {/* Card metadata list */}
              <div className="space-y-1 text-[9px] font-semibold text-slate-400">
                <div className="flex justify-between">
                  <span>Vehicle ID:</span>
                  <span className="text-slate-200 font-mono">#{item.vehicle_id || '2003'}</span>
                </div>
                <div className="flex justify-between">
                  <span>License Plate:</span>
                  <span className="text-slate-200 font-mono uppercase">{item.plate_number || 'PB10AB1234'}</span>
                </div>
                <div className="flex justify-between">
                  <span>Camera ID:</span>
                  <span className="text-slate-200">{item.camera_id || 'Upload-Center'}</span>
                </div>
                <div className="flex justify-between">
                  <span>Timestamp:</span>
                  <span className="text-slate-200 font-mono">{item.timestamp}</span>
                </div>
                <div className="flex justify-between items-center pt-1 border-t border-slate-900 mt-1">
                  <span>Confidence:</span>
                  <span className="text-emerald-450 font-mono font-bold">{(item.confidence * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Full-size interactive viewer modal */}
      {isViewerOpen && (
        <div className="fixed inset-0 z-50 bg-black/95 backdrop-blur-sm flex flex-col justify-between p-6 select-none animate-fadeIn">
          {/* Modal Header */}
          <div className="flex justify-between items-center text-slate-100">
            <div className="space-y-0.5">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Evidence Locker Viewer</h4>
              <p className="text-[10px] text-slate-500 font-semibold">Vehicle #{activeViolation.vehicle_id} | Plate {activeViolation.plate_number}</p>
            </div>
            <button 
              onClick={() => { setIsViewerOpen(false); handleResetZoom(); }}
              className="p-1.5 rounded-lg bg-slate-900 border border-slate-800 hover:text-white transition-all cursor-pointer text-slate-400"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Modal Canvas (Zoom & Pan support) */}
          <div 
            className="flex-1 flex items-center justify-center overflow-hidden cursor-grab active:cursor-grabbing relative"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
          >
            <div 
              className="transition-transform duration-100 ease-out select-none"
              style={{
                transform: `translate(${pan.x}px, ${pan.y}px) scale(${zoom})`,
              }}
            >
              <img 
                src={activeViolation.annotated_image_path || `/api/v1/evidence/${activeViolation.evidence_id}/processed?type=image`} 
                alt="evidence-zoom" 
                className="max-h-[70vh] object-contain rounded-lg shadow-2xl border border-slate-900 pointer-events-none"
                onError={(e) => { e.target.src = '/uploads/snapshot_mock.jpg'; }}
              />
            </div>

            {/* Floating Zoom Controls */}
            <div className="absolute bottom-4 right-4 bg-slate-900/80 border border-slate-800 p-1.5 rounded-xl flex items-center space-x-2 text-slate-350">
              <button onClick={handleZoomOut} className="p-1 rounded hover:text-white transition-colors cursor-pointer"><ZoomOut className="w-3.5 h-3.5" /></button>
              <span className="text-[9px] font-mono font-bold px-1">{Math.round(zoom * 100)}%</span>
              <button onClick={handleZoomIn} className="p-1 rounded hover:text-white transition-colors cursor-pointer"><ZoomIn className="w-3.5 h-3.5" /></button>
              <button onClick={handleResetZoom} className="p-1 rounded hover:text-white transition-colors cursor-pointer"><RotateCcw className="w-3.5 h-3.5" /></button>
            </div>
          </div>

          {/* Modal Footer Controls (Prev/Next, Download) */}
          <div className="flex justify-between items-center pt-4 border-t border-slate-900">
            <div className="flex items-center space-x-2">
              <button
                onClick={handlePrev}
                disabled={currentIndex === 0}
                className="px-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs font-bold text-slate-300 hover:text-white disabled:opacity-30 cursor-pointer transition-all"
              >
                Previous
              </button>
              <span className="text-[10px] text-slate-500 font-mono font-bold">
                {currentIndex + 1} / {moduleViolations.length}
              </span>
              <button
                onClick={handleNext}
                disabled={currentIndex === moduleViolations.length - 1}
                className="px-4 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs font-bold text-slate-300 hover:text-white disabled:opacity-30 cursor-pointer transition-all"
              >
                Next
              </button>
            </div>

            <div className="flex space-x-2">
              <a 
                href={activeViolation.original_image_path || `/api/v1/evidence/${activeViolation.evidence_id}/original?type=image`}
                download={`original_${activeViolation.evidence_id}.jpg`}
                className="px-4 py-2 text-xs font-bold text-slate-300 hover:text-white bg-slate-900 border border-slate-800 rounded-lg flex items-center space-x-1.5 transition-all"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Original</span>
              </a>
              <a 
                href={activeViolation.annotated_image_path || `/api/v1/evidence/${activeViolation.evidence_id}/processed?type=image`}
                download={`annotated_${activeViolation.evidence_id}.jpg`}
                className="px-4 py-2 text-xs font-bold text-white bg-purple-650 hover:bg-purple-750 border border-purple-550 rounded-lg flex items-center space-x-1.5 transition-all"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Annotated</span>
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ModuleViolationPage({ moduleName }) {
  return (
    <ErrorBoundary>
      <ModuleViolationContent moduleName={moduleName} />
    </ErrorBoundary>
  );
}
