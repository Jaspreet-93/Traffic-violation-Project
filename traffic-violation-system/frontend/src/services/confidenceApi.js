import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const confidenceAPI = {
  getLiveConfidence: () => API.get('/api/v1/confidence/live'),
  getHistory: () => API.get('/api/v1/confidence/history'),
  getModels: () => API.get('/api/v1/confidence/models'),
  getTrustScore: () => API.get('/api/v1/confidence/trust-score'),
  getStatistics: () => API.get('/api/v1/confidence/statistics'),
};

export default confidenceAPI;
