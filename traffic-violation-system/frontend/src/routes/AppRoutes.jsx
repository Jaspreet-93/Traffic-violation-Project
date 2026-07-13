import React, { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

const Login = lazy(() => import('../pages/Login'));
const Dashboard = lazy(() => import('../pages/Dashboard'));
const LiveMonitoring = lazy(() => import('../pages/LiveMonitoring'));
const UploadDetection = lazy(() => import('../pages/UploadDetection'));
const Violations = lazy(() => import('../pages/Violations'));
const Evidence = lazy(() => import('../pages/Evidence'));
const Settings = lazy(() => import('../pages/Settings'));
const ReplayCenter = lazy(() => import('../pages/ReplayCenter'));
const EvidenceLocker = lazy(() => import('../pages/EvidenceLocker'));
const CameraManagement = lazy(() => import('../pages/CameraManagement'));
const Reports = lazy(() => import('../pages/Reports'));
const Profile = lazy(() => import('../pages/Profile'));
const SystemDiagnostics = lazy(() => import('../pages/SystemDiagnostics'));
const ModuleViolationPage = lazy(() => import('../pages/ModuleViolationPage'));

export default function AppRoutes() {
  return (
    <Suspense fallback={
      <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-xs space-y-2">
        <span className="w-4 h-4 rounded-full border-2 border-purple-500 border-t-transparent animate-spin"></span>
        <span>Loading Interface Component...</span>
      </div>
    }>
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
    </Suspense>
  );
}
