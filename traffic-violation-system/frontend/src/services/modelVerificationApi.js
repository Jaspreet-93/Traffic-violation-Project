import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const modelVerificationAPI = {
  getOverview: () => API.get('/api/v1/model/overview'),
  getHealth: () => API.get('/api/v1/model/health'),
  getMetrics: () => API.get('/api/v1/model/metrics'),
  getDataset: () => API.get('/api/v1/model/dataset'),
  getPerformance: () => API.get('/api/v1/model/performance'),
  getBenchmark: () => API.get('/api/v1/model/benchmark'),
  getRecommendations: () => API.get('/api/v1/model/recommendations'),
  getVerification: () => API.get('/api/v1/model/verification'),
};

export default modelVerificationAPI;
