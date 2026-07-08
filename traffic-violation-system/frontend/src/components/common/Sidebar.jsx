import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, Radio, Upload, AlertOctagon, FileVideo, BarChart3, Settings, Mail, Cpu, Activity, GitPullRequest, Video, FileText, ShieldCheck, User, LogOut } from 'lucide-react';

const translations = {
  en: {
    dashboard: "Dashboard",
    liveMonitoring: "Live Monitoring",
    cameraManagement: "Camera Management",
    uploadDetection: "Upload Detection",
    violations: "Violations",
    evidenceLocker: "Evidence Locker",
    aiStatistics: "AI Statistics",
    aiVerification: "AI Verification",
    reportsCenter: "Reports Center",
    analyticsInsights: "Analytics Insights",
    aiCommandCenter: "AI Command Center",
    aiConfidence: "AI Confidence",
    decisionEngine: "Decision Engine",
    replayCenter: "Replay Center",
    profile: "Edit Profile / PW",
    settings: "System Settings",
    emailLogs: "Email Logs",
    logout: "Logout Session",
    console: "Monitor Console"
  },
  hi: {
    dashboard: "डैशबोर्ड",
    liveMonitoring: "लाइव निगरानी",
    cameraManagement: "कैमरा प्रबंधन",
    uploadDetection: "अपलोड डिटेक्शन",
    violations: "उल्लंघन",
    evidenceLocker: "साक्ष्य लॉकर",
    aiStatistics: "एआई सांख्यिकी",
    aiVerification: "एआई सत्यापन",
    reportsCenter: "रिपोर्ट केंद्र",
    analyticsInsights: "विश्लेषण अंतर्दृष्टि",
    aiCommandCenter: "एआई कमांड सेंटर",
    aiConfidence: "एआई आत्मविश्वास",
    decisionEngine: "निर्णय इंजन",
    replayCenter: "रीप्ले केंद्र",
    profile: "प्रोफ़ाइल संपादित करें",
    settings: "सिस्टम सेटिंग्स",
    emailLogs: "ईमेल लॉग",
    logout: "लॉगआउट",
    console: "निगरानी कंसोल"
  },
  es: {
    dashboard: "Tablero",
    liveMonitoring: "Monitoreo en Vivo",
    cameraManagement: "Gestión de Cámaras",
    uploadDetection: "Detección de Carga",
    violations: "Infracciones",
    evidenceLocker: "Casillero de Pruebas",
    aiStatistics: "Estadísticas de IA",
    aiVerification: "Verificación de IA",
    reportsCenter: "Centro de Reportes",
    analyticsInsights: "Información Analítica",
    aiCommandCenter: "Centro de Comando de IA",
    aiConfidence: "Confianza de IA",
    decisionEngine: "Motor de Decisiones",
    replayCenter: "Centro de Reproducción",
    profile: "Editar Perfil / Contraseña",
    settings: "Configuración del Sistema",
    emailLogs: "Registros de Correo",
    logout: "Cerrar Sesión",
    console: "Consola de Monitoreo"
  }
};

export default function Sidebar() {
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
    { path: '/ai-statistics', label: t.aiStatistics, icon: Activity },
    { path: '/model-verification', label: t.aiVerification, icon: ShieldCheck },
    { path: '/reports', label: t.reportsCenter, icon: FileText },
    { path: '/analytics', label: t.analyticsInsights, icon: BarChart3 },
    { path: '/ai-command-center', label: t.aiCommandCenter, icon: Cpu },
    { path: '/confidence-dashboard', label: t.aiConfidence, icon: Activity },
    { path: '/ai-decision-engine', label: t.decisionEngine, icon: GitPullRequest },
    { path: '/replay-center', label: t.replayCenter, icon: Video },
    { path: '/profile', label: t.profile, icon: User },
    { path: '/settings', label: t.settings, icon: Settings },
    { path: '/email-logs', label: t.emailLogs, icon: Mail },
  ];

  const handleLogout = () => {
    localStorage.removeItem('user_profile');
    localStorage.removeItem('admin_logged_in');
    navigate('/login');
  };

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-955 flex flex-col justify-between py-6 overflow-y-auto">
      <div className="space-y-6 px-4">
        <span className="text-[10px] font-bold text-slate-550 tracking-wider uppercase pl-2">{t.console}</span>
        <div className="space-y-1">
          {menuItems.map((item, idx) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={idx}
                to={item.path}
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
