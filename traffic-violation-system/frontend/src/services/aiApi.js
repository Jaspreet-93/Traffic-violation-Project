import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const aiAPI = {
  getOverview: () => API.get('/api/v1/ai/overview'),
  getModels: () => API.get('/api/v1/ai/models'),
  getModelHealth: () => API.get('/api/v1/ai/model-health'),
  getTrainingMetrics: () => API.get('/api/v1/ai/training-metrics'),
  getDatasets: () => API.get('/api/v1/ai/datasets'),
  getConfidence: () => API.get('/api/v1/ai/confidence'),
  getPerformance: () => API.get('/api/v1/ai/performance'),
  getBenchmark: () => API.get('/api/v1/ai/benchmark'),
  getSystemHealth: () => API.get('/api/v1/ai/system-health'),
  getDiagnostics: () => API.get('/api/v1/ai/diagnostics'),
  getRecommendations: () => API.get('/api/v1/ai/recommendations'),
  getReport: () => API.get('/api/v1/ai/report'),
  exportReport: (format) => API.post('/api/v1/ai/report/export', { format }),
};
