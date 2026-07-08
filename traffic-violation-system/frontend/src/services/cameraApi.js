import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const cameraAPI = {
  getAll: () => API.get('/api/v1/cameras'),
  create: (data) => API.post('/api/v1/cameras', data),
  update: (id, data) => API.put(`/api/v1/cameras/${id}`, data),
  delete: (id) => API.delete(`/api/v1/cameras/${id}`),
  getStatus: () => API.get('/api/v1/cameras/status'),
  getHealth: (id) => API.get(`/api/v1/cameras/health/${id}`),
};

export default cameraAPI;
