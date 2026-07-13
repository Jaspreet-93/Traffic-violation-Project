import React, { createContext, useState, useEffect, useContext } from 'react';
import { systemAPI } from '../services/api';

const SystemContext = createContext(null);

export function SystemProvider({ children }) {
  const [healthData, setHealthData] = useState({
    status: 'Healthy',
    services: {
      backend: 'Online',
      database: 'Online',
      models_loaded: 'Online',
      camera_service: 'Online',
      video_engine: 'Online',
      detection_engine: 'Online',
      ocr_engine: 'Online',
      evidence_storage: 'Online',
      report_service: 'Online',
      websocket: 'Online'
    },
    diagnostics: {
      uptime: 0,
      api_response_time: '0ms',
      database_latency: '0ms',
      inference_speed_fps: '32 FPS',
      active_cameras: 0,
      connected_clients: 0,
      cpu_usage: '0%',
      ram_usage: '0%',
      gpu_usage: 'N/A',
      disk_usage: '0%',
      storage_remaining_gb: '0 GB',
      last_health_check: ''
    },
    recent_errors: []
  });

  const [loading, setLoading] = useState(true);

  const fetchHealth = async () => {
    try {
      const res = await systemAPI.getHealth();
      if (res.data) {
        setHealthData(res.data);
      }
    } catch (err) {
      console.error("Health check fetch failed (Backend Offline):", err);
      setHealthData(prev => ({
        ...prev,
        status: 'Backend Offline',
        services: Object.keys(prev.services).reduce((acc, key) => {
          acc[key] = key === 'backend' ? 'Offline' : 'Unknown';
          return acc;
        }, {})
      }));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealth();
    const interval = setInterval(fetchHealth, 5000);

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    const wsHost = host.includes('3000') ? 'localhost:8000' : host;
    const wsUrl = `${protocol}//${wsHost}/api/v1/ws`;

    let ws;
    const connectWS = () => {
      ws = new WebSocket(wsUrl);
      ws.onopen = () => {
        console.log("WebSocket connected to backend diagnostics.");
      };
      ws.onclose = () => {
        console.log("WebSocket connection closed, retrying in 5s...");
        setTimeout(connectWS, 5000);
      };
      ws.onerror = (err) => {
        ws.close();
      };
    };

    connectWS();

    return () => {
      clearInterval(interval);
      if (ws) ws.close();
    };
  }, []);

  return (
    <SystemContext.Provider value={{ healthData, refreshHealth: fetchHealth, loading }}>
      {children}
    </SystemContext.Provider>
  );
}

export function useSystem() {
  const context = useContext(SystemContext);
  if (!context) {
    throw new Error('useSystem must be used within a SystemProvider');
  }
  return context;
}
