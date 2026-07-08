import React, { useState } from 'react';
import FileUploader from '../components/upload/FileUploader';
import ImagePreview from '../components/upload/ImagePreview';
import VideoPreview from '../components/upload/VideoPreview';
import DetectionResult from '../components/upload/DetectionResult';
import { detectionAPI } from '../services/api';

export default function UploadDetection() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState(null); // API response object
  const [fileType, setFileType] = useState(null); // 'image' or 'video'
  const [videoStreaming, setVideoStreaming] = useState(false);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setResult(null);
      setVideoStreaming(false);
      
      if (file.type.startsWith('image/')) {
        setFileType('image');
      } else if (file.type.startsWith('video/')) {
        setFileType('video');
      } else {
        setFileType(null);
      }
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile || !fileType) return;

    try {
      setUploading(true);
      setResult(null);
      setVideoStreaming(false);

      if (fileType === 'image') {
        const res = await detectionAPI.uploadImage(selectedFile);
        if (res.data.error) {
          alert("Error: " + res.data.error);
        } else {
          setResult(res.data);
        }
      } else if (fileType === 'video') {
        const res = await detectionAPI.uploadVideo(selectedFile);
        if (res.data.error) {
          alert("Error: " + res.data.error);
        } else {
          setResult(res.data);
          setVideoStreaming(true);
        }
      }
    } catch (err) {
      alert("Analysis failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 p-6 space-y-6 overflow-y-auto">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-100">Upload Violation Detection</h2>
        <p className="text-xs text-slate-500">Run computer vision inference on custom images and videos to verify traffic infractions.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Col: Uploader controls */}
        <div className="lg:col-span-1">
          <FileUploader
            selectedFile={selectedFile}
            handleFileChange={handleFileChange}
            handleUpload={handleUpload}
            uploading={uploading}
          />
        </div>

        {/* Right Col: Preview results */}
        <div className="lg:col-span-2 space-y-6">
          {/* Render visual preview blocks */}
          {fileType === 'image' && result && (
            <ImagePreview originalFile={selectedFile} processedPath={result.processed_file} />
          )}

          {fileType === 'video' && videoStreaming && (
            <VideoPreview originalFile={selectedFile} streamActive={videoStreaming} />
          )}

          {/* Render detection stats metrics details */}
          {result && (
            <DetectionResult result={result} />
          )}

          {/* Blank placeholder if no action was triggered */}
          {!result && (
            <div className="bg-slate-900/50 border border-slate-800 border-dashed rounded-xl p-12 text-center text-slate-500 flex flex-col items-center justify-center min-h-[350px]">
              <Upload className="w-12 h-12 text-slate-850 mb-3" />
              <h4 className="text-slate-400 font-medium">No Active Analysis</h4>
              <p className="text-xs text-slate-655 mt-1">Select an image or video file on the left and click submit to run detections.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
// Import Helper Upload icon from Lucide for placeholder
import { Upload } from 'lucide-react';
