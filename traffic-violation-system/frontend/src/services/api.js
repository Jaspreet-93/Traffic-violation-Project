import axios from 'axios';

// All requests are proxied via Vite config to http://localhost:8000
const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const cameraAPI = {
  getStatus: () => API.get('/api/v1/camera/status'),
  startStream: (source) => API.post('/api/v1/camera/start', { source }),
  stopStream: () => API.post('/api/v1/camera/stop'),
  uploadFile: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return API.post('/api/v1/camera/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};

export const pipelineAPI = {
  getTrackingStatus: () => API.get('/api/v1/tracking/status'),
  startTracking: () => API.post('/api/v1/tracking/start'),
  stopTracking: () => API.post('/api/v1/tracking/stop'),

  getHelmetStatus: () => API.get('/api/v1/helmet/status'),
  startHelmet: () => API.post('/api/v1/helmet/start'),
  stopHelmet: () => API.post('/api/v1/helmet/stop'),

  getPlateStatus: () => API.get('/api/v1/number-plate/status'),
  startPlate: () => API.post('/api/v1/number-plate/start'),
  stopPlate: () => API.post('/api/v1/number-plate/stop'),

  getOCRStatus: () => API.get('/api/v1/ocr/status'),
  startOCR: () => API.post('/api/v1/ocr/start'),
  stopOCR: () => API.post('/api/v1/ocr/stop'),

  getSeatBeltStatus: () => API.get('/api/v1/seat-belt/status'),
  startSeatBelt: () => API.post('/api/v1/seat-belt/start'),
  stopSeatBelt: () => API.post('/api/v1/seat-belt/stop'),

  getTrafficLightStatus: () => API.get('/api/v1/traffic-light/status'),
  startTrafficLight: () => API.post('/api/v1/traffic-light/start'),
  stopTrafficLight: () => API.post('/api/v1/traffic-light/stop'),

  getBehaviorStatus: () => API.get('/api/v1/driver-behavior/status'),
  startBehavior: () => API.post('/api/v1/driver-behavior/start'),
  stopBehavior: () => API.post('/api/v1/driver-behavior/stop'),
};

export const violationAPI = {
  getAll: () => API.get('/api/v1/violations'),
  getByVehicle: (vehicleId) => API.get(`/api/v1/violations/${vehicleId}`),
};

export const evidenceAPI = {
  getAll: () => API.get('/api/v1/evidence'),
  getByViolation: (violationId) => API.get(`/api/v1/evidence/${violationId}`),
};

export const analyticsAPI = {
  getSummary: () => API.get('/api/v1/analytics/summary'),
  getDaily: () => API.get('/api/v1/analytics/daily'),
  getTypes: () => API.get('/api/v1/analytics/types'),
};

export default API;
