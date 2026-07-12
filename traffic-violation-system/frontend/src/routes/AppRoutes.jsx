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
import Reports from '../pages/Reports';
import Profile from '../pages/Profile';
import SystemDiagnostics from '../pages/SystemDiagnostics';
import ModuleViolationPage from '../pages/ModuleViolationPage';

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
      <Route path="/reports" element={<Reports />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/replay-center" element={<ReplayCenter />} />
      <Route path="/system-diagnostics" element={<SystemDiagnostics />} />
      
      {/* AI Decision Engine Subsystem Routes */}
      <Route path="/helmet-detection" element={<ModuleViolationPage moduleName="Helmet Detection" />} />
      <Route path="/seatbelt-detection" element={<ModuleViolationPage moduleName="Seat Belt Detection" />} />
      <Route path="/traffic-light" element={<ModuleViolationPage moduleName="Traffic Light" />} />
      <Route path="/speed-detection" element={<ModuleViolationPage moduleName="Speed Detection" />} />
      <Route path="/mobile-phone" element={<ModuleViolationPage moduleName="Mobile Phone" />} />
      <Route path="/triple-riding" element={<ModuleViolationPage moduleName="Triple Riding" />} />
      <Route path="/wrong-lane" element={<ModuleViolationPage moduleName="Wrong Lane" />} />
      <Route path="/stop-line" element={<ModuleViolationPage moduleName="Stop Line" />} />
      <Route path="/parking-violation" element={<ModuleViolationPage moduleName="Parking Violation" />} />
      <Route path="/number-plate-ocr" element={<ModuleViolationPage moduleName="Number Plate OCR" />} />
      
      {/* Fallback */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
