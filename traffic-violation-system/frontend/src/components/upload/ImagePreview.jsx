import React from 'react';
import { CheckCircle } from 'lucide-react';

export default function ImagePreview({ originalFile, processedPath }) {
  const [origUrl, setOrigUrl] = React.useState(null);

  React.useEffect(() => {
    if (originalFile) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setOrigUrl(reader.result);
      };
      reader.readAsDataURL(originalFile);
    } else {
      setOrigUrl(null);
    }
  }, [originalFile]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-2xl">
      {/* Before / Original */}
      <div className="flex flex-col">
        <h4 className="text-xs font-bold text-slate-500 uppercase mb-3">Original Image</h4>
        <div className="bg-slate-950 rounded-lg p-2 aspect-video flex items-center justify-center border border-slate-850 overflow-hidden">
          {origUrl ? (
            <img src={origUrl} alt="Original uploaded file" className="max-h-[300px] object-contain rounded" />
          ) : (
            <span className="text-xs text-slate-700">No original image loaded</span>
          )}
        </div>
      </div>

      {/* After / Processed */}
      <div className="flex flex-col">
        <h4 className="text-xs font-bold text-purple-400 uppercase mb-3 flex items-center space-x-1.5">
          <CheckCircle className="w-4 h-4 text-emerald-500" />
          <span>AI Processed Output</span>
        </h4>
        <div className="bg-slate-955 rounded-lg p-2 aspect-video flex items-center justify-center border border-purple-500/10 overflow-hidden">
          {processedPath ? (
            <img src={`/${processedPath}`} alt="Processed output" className="max-h-[300px] object-contain rounded" />
          ) : (
            <span className="text-xs text-slate-750">Pending AI analysis...</span>
          )}
        </div>
      </div>
    </div>
  );
}
