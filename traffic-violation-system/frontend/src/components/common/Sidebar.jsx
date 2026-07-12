import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Radio, Upload, AlertOctagon, FileVideo, Settings, Cpu, Activity, Video, FileText, ShieldCheck, User, LogOut, X } from 'lucide-react';

const translations = {
  en: {
    dashboard: "Dashboard",
    liveMonitoring: "Live Monitoring",
    cameraManagement: "Camera Management",
    uploadDetection: "Upload Image / Video",
    violations: "Violations",
    evidenceLocker: "Evidence Locker",
    aiStatistics: "AI Statistics",
    aiVerification: "AI Verification",
    reportsCenter: "Reports Center",
    replayCenter: "Replay Center",
    profile: "Edit Profile / PW",
    settings: "System Settings",
    logout: "Logout Session",
    console: "Monitor Console",
    systemDiagnostics: "System Diagnostics"
  },
  hi: {
    dashboard: "डैशबोर्ड",
    liveMonitoring: "लाइव निगरानी",
    cameraManagement: "कैमरा प्रबंधन",
    uploadDetection: "छवि / वीडियो अपलोड करें",
    violations: "उल्लंघन",
    evidenceLocker: "साक्ष्य लॉकर",
    aiStatistics: "एआई सांख्यिकी",
    aiVerification: "एआई सत्यापन",
    reportsCenter: "रिपोर्ट केंद्र",
    replayCenter: "रीप्ले केंद्र",
    profile: "प्रोफ़ाइल संपादित करें",
    settings: "सिस्टम सेटिंग्स",
    logout: "लॉगआउट",
    console: "निगरानी कंसोल",
    systemDiagnostics: "सिस्टम डायग्नोस्टिक्स"
  },
  es: {
    dashboard: "Tablero",
    liveMonitoring: "Monitoreo en Vivo",
    cameraManagement: "Gestión de Cámaras",
    uploadDetection: "Subir Imagen / Video",
    violations: "Infracciones",
    evidenceLocker: "Casillero de Pruebas",
    aiStatistics: "Estadísticas de IA",
    aiVerification: "Verificación de IA",
    reportsCenter: "Centro de Reportes",
    replayCenter: "Centro de Reproducción",
    profile: "Editar Perfil / Contraseña",
    settings: "Configuración del Sistema",
    logout: "Cerrar Sesión",
    console: "Consola de Monitoreo",
    systemDiagnostics: "Diagnósticos del Sistema"
  }
};

export default function Sidebar({ isOpen, onClose }) {
  const navigate = useNavigate();
  const lang = localStorage.getItem('system_language') || 'en';
  const t = translations[lang] || translations.en;

  const menuItems = [
    { path: '/dashboard', label: t.dashboard, icon: LayoutDashboard },
    { path: '/live-monitoring', label: t.liveMonitoring, icon: Radio },
    { path: '/camera-management', label: t.cameraManagement, icon: Video },
    { path: '/upload-detection', label: t.uploadDetection, icon: Upload },
    { path: '/violations', label: t.violations, icon: AlertOctagon },
    { path: '/evidence-locker', label: t.evidenceLocker, icon: FileVideo },
    { path: '/reports', label: t.reportsCenter, icon: FileText },
    { path: '/replay-center', label: t.replayCenter, icon: Video },
    { path: '/system-diagnostics', label: t.systemDiagnostics, icon: Activity },
    { path: '/profile', label: t.profile, icon: User },
    { path: '/settings', label: t.settings, icon: Settings },
  ];

  const handleLogout = () => {
    localStorage.removeItem('user_profile');
    localStorage.removeItem('admin_logged_in');
    navigate('/login');
  };

  return (
    <aside 
      className={`fixed lg:static top-0 bottom-0 left-0 w-64 border-r border-slate-800 bg-slate-950 flex flex-col justify-between py-6 overflow-y-auto z-40 transition-transform duration-300 lg:translate-x-0 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}
    >
      <div className="space-y-6 px-4">
        <div className="flex items-center justify-between pl-2">
          <span className="text-[10px] font-bold text-slate-555 tracking-wider uppercase">{t.console}</span>
          <button 
            onClick={onClose}
            className="p-1 rounded text-slate-500 hover:text-slate-350 lg:hidden cursor-pointer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        <div className="space-y-1">
          {menuItems.map((item, idx) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={idx}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `w-full flex items-center space-x-3 px-4 py-2 rounded text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-purple-650 text-white shadow-lg shadow-purple-650/20'
                      : 'text-slate-450 hover:bg-slate-900 hover:text-slate-200'
                  }`
                }
              >
                <Icon className="w-4 h-4" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </div>
      </div>

      <div className="px-4 py-4 border-t border-slate-900 mt-6 space-y-3">
        <button
          onClick={handleLogout}
          className="w-full flex items-center space-x-3 px-4 py-2 rounded text-xs font-semibold text-rose-450 hover:bg-rose-500/5 transition-colors cursor-pointer"
        >
          <LogOut className="w-4 h-4" />
          <span>{t.logout}</span>
        </button>

        <div className="flex items-center space-x-2 text-[10px] text-slate-600 pl-2">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>AURA Engine v1.0.0</span>
        </div>
      </div>
    </aside>
  );
}
