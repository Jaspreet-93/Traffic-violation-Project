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
      <Route path="/analytics" element={<Analytics />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/email-logs" element={<EmailLogs />} />
      <Route path="/ai-command-center" element={<AICommandCenter />} />
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
