import React, { createContext, useContext, useState, useEffect } from 'react';
import { uploadDetectionAPI } from '../services/uploadDetectionApi';

const UploadContext = createContext(null);

export function UploadProvider({ children }) {
  const [jobId, setJobId] = useState(() => localStorage.getItem('upload_job_id') || null);
  const [status, setStatus] = useState(() => localStorage.getItem('upload_status') || null);
  const [progress, setProgress] = useState(() => {
    const p = localStorage.getItem('upload_progress');
    return p ? parseFloat(p) : 0.0;
  });
  const [result, setResult] = useState(() => {
    const r = localStorage.getItem('upload_result');
    return r ? JSON.parse(r) : null;
  });
  const [processing, setProcessing] = useState(() => {
    const p = localStorage.getItem('upload_processing');
    return p === 'true';
  });
  const [loading, setLoading] = useState(false);
  const [jobStatus, setJobStatus] = useState(null);
  const [viewedResult, setViewedResult] = useState(() => {
    const vr = localStorage.getItem('upload_viewed_result');
    return vr ? JSON.parse(vr) : null;
  });

  // Sync to localStorage
  useEffect(() => {
    if (jobId) localStorage.setItem('upload_job_id', jobId);
    else localStorage.removeItem('upload_job_id');
  }, [jobId]);

  useEffect(() => {
    if (status) localStorage.setItem('upload_status', status);
    else localStorage.removeItem('upload_status');
  }, [status]);

  useEffect(() => {
    localStorage.setItem('upload_progress', progress.toString());
  }, [progress]);

  useEffect(() => {
    if (result) localStorage.setItem('upload_result', JSON.stringify(result));
    else localStorage.removeItem('upload_result');
  }, [result]);

  useEffect(() => {
    if (viewedResult) localStorage.setItem('upload_viewed_result', JSON.stringify(viewedResult));
    else localStorage.removeItem('upload_viewed_result');
  }, [viewedResult]);

  useEffect(() => {
    localStorage.setItem('upload_processing', processing ? 'true' : 'false');
  }, [processing]);

  // Polling loop inside the global provider so it never unmounts
  useEffect(() => {
    if (!jobId || status !== 'Processing') return;

    const interval = setInterval(async () => {
      try {
        const res = await uploadDetectionAPI.getStatus(jobId);
        setJobStatus(res.data);
        setProgress(res.data.progress);
        if (res.data.status === 'Completed') {
          setStatus('Completed');
          setProcessing(false);
          clearInterval(interval);
          const resRes = await uploadDetectionAPI.getResult(jobId);
          setResult(resRes.data);
          setViewedResult(resRes.data); // Set viewed result to completed output
        } else if (res.data.status === 'Failed') {
          setStatus('Failed');
          setProcessing(false);
          clearInterval(interval);
        }
      } catch (err) {
        console.error("Global polling error:", err);
        clearInterval(interval);
      }
    }, 1500);

    return () => clearInterval(interval);
  }, [jobId, status]);

  const uploadAndAnalyze = async (file) => {
    if (!file) return;
    setLoading(true);
    setResult(null);
    setViewedResult(null);
    setJobId(null);
    setStatus(null);
    setProgress(0.0);
    setProcessing(false);

    const formData = new FormData();
    formData.append('file', file);

    const name = file.name.toLowerCase();
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
        const resRes = await uploadDetectionAPI.getResult(jId);
        setResult(resRes.data);
        setViewedResult(resRes.data);
      }
    } catch (err) {
      console.error("Global upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  const clearUploadState = () => {
    setJobId(null);
    setStatus(null);
    setProgress(0.0);
    setResult(null);
    setViewedResult(null);
    setProcessing(false);
    setLoading(false);
  };

  return (
    <UploadContext.Provider value={{
      jobId, setJobId,
      status, setStatus,
      progress, setProgress,
      result, setResult,
      viewedResult, setViewedResult,
      processing, setProcessing,
      loading, setLoading,
      jobStatus, setJobStatus,
      uploadAndAnalyze,
      clearUploadState
    }}>
      {children}
    </UploadContext.Provider>
  );
}

export function useUpload() {
  return useContext(UploadContext);
}
