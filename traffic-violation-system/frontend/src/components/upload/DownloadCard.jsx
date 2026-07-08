import React from 'react';
import { Download, FileText, FileVideo, FileImage } from 'lucide-react';

export default function DownloadCard({ result }) {
  if (!result) return null;

  const outUrl = result.evidence.processed_file_url || '';
  const isVideo = result.file_type === 'video';

  const downloadTextSummary = () => {
    const content = `AURA SURVEILLANCE REPORT\nJob ID: ${result.job_id}\nFile: ${result.filename}\nType: ${result.file_type}\n\nSummary:\n${result.evidence.summary_text}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `detection_summary_${result.job_id}.txt`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 shadow space-y-4">
      <h4 className="text-xs font-bold text-slate-555 uppercase tracking-wider">Export Results</h4>

      <div className="flex gap-4">
        {outUrl && (
          <a
            href={outUrl}
            download={`processed_${result.filename}`}
            className="flex-1 bg-purple-650 hover:bg-purple-750 text-white font-semibold py-2.5 rounded-lg text-xs flex items-center justify-center space-x-1.5 shadow transition-all cursor-pointer"
          >
            {isVideo ? <FileVideo className="w-3.5 h-3.5" /> : <FileImage className="w-3.5 h-3.5" />}
            <span>Download Processed Media</span>
          </a>
        )}

        <button
          onClick={downloadTextSummary}
          className="flex-1 bg-slate-950 hover:bg-slate-950/80 border border-slate-800 text-slate-350 font-semibold py-2.5 rounded-lg text-xs flex items-center justify-center space-x-1.5 transition-all cursor-pointer"
        >
          <FileText className="w-3.5 h-3.5" />
          <span>Download Summary Report</span>
        </button>
      </div>
    </div>
  );
}
// Import file schemas
import { FileCode } from 'lucide-react';
