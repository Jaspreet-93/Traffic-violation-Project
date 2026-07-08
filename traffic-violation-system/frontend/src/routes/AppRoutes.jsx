import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import LiveMonitoring from '../pages/LiveMonitoring';
import UploadDetection from '../pages/UploadDetection';
import Violations from '../pages/Violations';
import Evidence from '../pages/Evidence';
import Settings from '../pages/Settings';
import ReplayCenter from '../pages/ReplayCenter';
import EvidenceLocker from '../pages/EvidenceLocker';
import CameraManagement from '../pages/CameraManagement';
import AIStatistics from '../pages/AIStatistics';
import Reports from '../pages/Reports';
import ModelVerification from '../pages/ModelVerification';
import Profile from '../pages/Profile';

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/live-monitoring" element={<LiveMonitoring />} />
      <Route path="/upload-detection" element={<UploadDetection />} />
      <Route path="/violations" element={<Violations />} />
      <Route path="/evidence" element={<Evidence />} />
      <Route path="/evidence-locker" element={<EvidenceLocker />} />
      <Route path="/camera-management" element={<CameraManagement />} />
      <Route path="/ai-statistics" element={<AIStatistics />} />
      <Route path="/reports" element={<Reports />} />
      <Route path="/model-verification" element={<ModelVerification />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/replay-center" element={<ReplayCenter />} />
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
