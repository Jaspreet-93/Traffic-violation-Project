import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import LiveMonitoring from '../pages/LiveMonitoring';
import UploadDetection from '../pages/UploadDetection';
import Violations from '../pages/Violations';
import Evidence from '../pages/Evidence';
import Analytics from '../pages/Analytics';
import Settings from '../pages/Settings';
import EmailLogs from '../pages/EmailLogs';
import AICommandCenter from '../pages/AICommandCenter';
import ConfidenceDashboard from '../pages/ConfidenceDashboard';
import AIDecisionEngine from '../pages/AIDecisionEngine';
import ReplayCenter from '../pages/ReplayCenter';
import EvidenceLocker from '../pages/EvidenceLocker';

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
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/email-logs" element={<EmailLogs />} />
      <Route path="/ai-command-center" element={<AICommandCenter />} />
      <Route path="/confidence-dashboard" element={<ConfidenceDashboard />} />
      <Route path="/ai-decision-engine" element={<AIDecisionEngine />} />
      <Route path="/replay-center" element={<ReplayCenter />} />
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
