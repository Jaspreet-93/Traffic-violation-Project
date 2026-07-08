import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const aiCommandCenterAPI = {
  getOverview: () => API.get('/api/v1/ai/overview'),
  getSystemHealth: () => API.get('/api/v1/ai/system-health'),
  getModelHealth: () => API.get('/api/v1/ai/model-health'),
  getHardware: () => API.get('/api/v1/ai/hardware'),
  getConfidence: () => API.get('/api/v1/ai/confidence'),
  getPerformance: () => API.get('/api/v1/ai/performance'),
};
export default aiCommandCenterAPI;
