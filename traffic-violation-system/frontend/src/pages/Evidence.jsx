import React, { useState, useEffect } from 'react';
import { Play, FileText, Image } from 'lucide-react';
import { evidenceAPI } from '../services/api';
import EvidenceViewer from '../components/EvidenceViewer';

export default function Evidence() {
  const [evidenceList, setEvidenceList] = useState([]);
  const [selectedViolationId, setSelectedViolationId] = useState(null);

  useEffect(() => {
    fetchEvidence();
  }, []);

  const fetchEvidence = async () => {
    try {
      const res = await evidenceAPI.getAll();
      setEvidenceList(res.data.reverse()); // latest first
    } catch (err) {
      console.error("Error loading evidence vault:", err);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Evidence Vault</h2>
        <p className="text-xs text-slate-500">Review JPG snapshots and MP4 video recordings of verified violation infractions.</p>
      </div>

      {evidenceList.length === 0 ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-12 text-center text-slate-500 flex flex-col items-center justify-center min-h-[300px]">
          <Image className="w-12 h-12 text-slate-800 mb-3" />
          <p className="font-semibold text-slate-400">Evidence Vault Empty</p>
          <p className="text-xs text-slate-650 mt-1">Start camera stream and trigger violations to store image and video proof.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {evidenceList.map((item, idx) => (
            <div
              key={idx}
              onClick={() => setSelectedViolationId(item.vehicle_id)} // map vehicle_id search target
              className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-all cursor-pointer group flex flex-col"
            >
              {/* Image Preview container */}
              <div className="bg-slate-950 aspect-video relative overflow-hidden flex items-center justify-center">
                <img
                  src={`/${item.image_path}`}
                  alt="Evidence snapshot"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <div className="bg-purple-600 p-3 rounded-full text-white shadow-lg">
                    <Play className="w-5 h-5 fill-current" />
                  </div>
                </div>
              </div>

              {/* Meta details footer */}
              <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-bold text-slate-200">Vehicle #{item.vehicle_id}</h4>
                    <span className="text-[10px] font-mono text-slate-500 uppercase">License: {item.plate_number || 'PB10AB1234'}</span>
                  </div>
                  <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border border-purple-500/20 bg-purple-500/5 text-purple-400">
                    {item.violation}
                  </span>
                </div>
                
                <span className="text-[10px] text-slate-500 block pt-2 border-t border-slate-850">
                  Captured: {item.timestamp}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal viewer popup */}
      {selectedViolationId && (
        <EvidenceViewer
          violationId={selectedViolationId}
          onClose={() => setSelectedViolationId(null)}
        />
      )}
    </div>
  );
}
