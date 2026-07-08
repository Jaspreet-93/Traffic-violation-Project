import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const decisionAPI = {
  getLatest: () => API.get('/api/v1/decision/latest'),
  getDecisionById: (id) => API.get(`/api/v1/decision/${id}`),
  getHistory: () => API.get('/api/v1/decision/history'),
  getExplanation: (id) => API.get(`/api/v1/decision/explanation/${id}`),
  getAudit: (id) => API.get(`/api/v1/decision/audit/${id}`),
};

export default decisionAPI;
