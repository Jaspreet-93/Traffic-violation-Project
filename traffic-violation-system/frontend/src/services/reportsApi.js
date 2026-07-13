import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const reportsAPI = {
  getAll: (page = 1, limit = 20) => API.get('/api/v1/reports', { params: { page, limit } }),
  generate: (data) => API.post('/api/v1/reports/generate', data),
  delete: (id) => API.delete(`/api/v1/reports/${id}`),
  getDownloadUrl: (id) => `/api/v1/reports/${id}`,
};

export default reportsAPI;
