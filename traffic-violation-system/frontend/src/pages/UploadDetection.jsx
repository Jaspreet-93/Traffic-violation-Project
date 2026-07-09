import React, { useState, useEffect } from 'react';
import { uploadDetectionAPI } from '../services/uploadDetectionApi';
import { useUpload } from '../context/UploadContext';
import UploadArea from '../components/upload/UploadArea';
import ImagePreview from '../components/upload/ImagePreview';
import VideoPreview from '../components/upload/VideoPreview';
import DetectionResult from '../components/upload/DetectionResult';
import DetectionSummary from '../components/upload/DetectionSummary';
import ProgressCard from '../components/upload/ProgressCard';
import DownloadCard from '../components/upload/DownloadCard';
import UploadHistory from '../components/upload/UploadHistory';

export default function UploadDetection() {
  const {
    jobId,
    progress,
    viewedResult, setViewedResult,
    processing,
    loading,
    uploadAndAnalyze,
    clearUploadState
  } = useUpload();

  const [selectedFile, setSelectedFile] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchHistory = async () => {
    try {
      const res = await uploadDetectionAPI.getHistory();
      setHistory(res.data.history || []);
    } catch (err) {
      console.error("Failed to load upload logs:", err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleFileSelected = (file) => {
    setSelectedFile(file);
    clearUploadState();
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) return;
    await uploadAndAnalyze(selectedFile);
    fetchHistory();
  };

  const handleViewResult = async (jId) => {
    try {
      const res = await uploadDetectionAPI.getResult(jId);
      setViewedResult(res.data); // Set viewed result only, do not touch active upload states!
      setSelectedFile(null);
    } catch (err) {
      console.error("View result fail:", err);
    }
  };

  const handleDeleteHistory = async (jId) => {
    try {
      await uploadDetectionAPI.deleteHistory(jId);
      if (jobId === jId) {
        clearUploadState();
      }
      fetchHistory();
    } catch (err) {
      console.error("Delete history entry fail:", err);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100 font-sans">Upload Detection Center</h2>
        <p className="text-xs text-slate-500">Process intersection video files and snapshots through YOLOv8 computer vision classifiers.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Upload Area */}
          <UploadArea onFileSelected={handleFileSelected} />

          {/* Action Trigger */}
          {selectedFile && !processing && (
            <button
              onClick={handleUploadAndAnalyze}
              disabled={loading}
              className="w-full bg-purple-650 hover:bg-purple-750 disabled:opacity-50 text-white font-semibold py-3 rounded-xl transition-all shadow-md text-xs cursor-pointer"
            >
              {loading ? "Analyzing..." : "Analyze Media File"}
            </button>
          )}

          {/* Progress bar */}
          {processing && <ProgressCard progress={progress} />}

          {/* Results Canvas */}
          {viewedResult && <DetectionResult result={viewedResult} />}
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          {/* Preview */}
          {selectedFile && !viewedResult && !processing && (
            selectedFile.name.toLowerCase().endsWith('.mp4') ||
            selectedFile.name.toLowerCase().endsWith('.avi') ||
            selectedFile.name.toLowerCase().endsWith('.mov') ||
            selectedFile.name.toLowerCase().endsWith('.mkv') ? (
              <VideoPreview file={selectedFile} onClear={() => setSelectedFile(null)} />
            ) : (
              <ImagePreview file={selectedFile} onClear={() => setSelectedFile(null)} />
            )
          )}

          {/* Summary counters */}
          {viewedResult && <DetectionSummary evidence={viewedResult.evidence} />}

          {/* Download card */}
          {viewedResult && <DownloadCard result={viewedResult} />}
        </div>
      </div>

      {/* History log list */}
      <UploadHistory
        historyList={history}
        onView={handleViewResult}
        onDelete={handleDeleteHistory}
      />
    </div>
  );
}
