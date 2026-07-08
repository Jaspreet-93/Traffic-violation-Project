import React, { useState, useEffect } from 'react';
import { uploadDetectionAPI } from '../services/uploadDetectionApi';
import UploadArea from '../components/upload/UploadArea';
import ImagePreview from '../components/upload/ImagePreview';
import VideoPreview from '../components/upload/VideoPreview';
import DetectionResult from '../components/upload/DetectionResult';
import DetectionSummary from '../components/upload/DetectionSummary';
import ProgressCard from '../components/upload/ProgressCard';
import DownloadCard from '../components/upload/DownloadCard';
import UploadHistory from '../components/upload/UploadHistory';

export default function UploadDetection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [progress, setProgress] = useState(0.0);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);

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

  // Poll video status
  useEffect(() => {
    if (!jobId || status !== 'Processing') return;

    const interval = setInterval(async () => {
      try {
        const res = await uploadDetectionAPI.getStatus(jobId);
        setProgress(res.data.progress);
        if (res.data.status === 'Completed') {
          setStatus('Completed');
          setProcessing(false);
          clearInterval(interval);
          // Fetch results
          const resRes = await uploadDetectionAPI.getResult(jobId);
          setResult(resRes.data);
          fetchHistory();
        } else if (res.data.status === 'Failed') {
          setStatus('Failed');
          setProcessing(false);
          clearInterval(interval);
          fetchHistory();
        }
      } catch (err) {
        console.error("Error polling job status:", err);
        clearInterval(interval);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [jobId, status]);

  const handleFileSelected = (file) => {
    setSelectedFile(file);
    setJobId(null);
    setStatus(null);
    setProgress(0.0);
    setResult(null);
  };

  const handleUploadAndAnalyze = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    const name = selectedFile.name.toLowerCase();
    const isVideo = ['.mp4', '.avi', '.mov', '.mkv'].some(ext => name.endsWith(ext));

    try {
      let res;
      if (isVideo) {
        res = await uploadDetectionAPI.uploadVideo(formData);
        setJobId(res.data.job_id);
        setStatus('Processing');
        setProcessing(true);
      } else {
        res = await uploadDetectionAPI.uploadImage(formData);
        const jId = res.data.job_id;
        setJobId(jId);
        setStatus('Completed');
        // Fetch results
        const resRes = await uploadDetectionAPI.getResult(jId);
        setResult(resRes.data);
        fetchHistory();
      }
    } catch (err) {
      console.error("Upload fail:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewResult = async (jId) => {
    try {
      const res = await uploadDetectionAPI.getResult(jId);
      setResult(res.data);
      setJobId(jId);
      setStatus('Completed');
      setSelectedFile(null);
    } catch (err) {
      console.error("View result fail:", err);
    }
  };

  const handleDeleteHistory = async (jId) => {
    try {
      await uploadDetectionAPI.deleteHistory(jId);
      if (jobId === jId) {
        setResult(null);
        setJobId(null);
        setStatus(null);
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
          {result && <DetectionResult result={result} />}
        </div>

        {/* Right (1 col) */}
        <div className="space-y-6">
          {/* Preview */}
          {selectedFile && !result && !processing && (
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
          {result && <DetectionSummary evidence={result.evidence} />}

          {/* Download card */}
          {result && <DownloadCard result={result} />}
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
