import axios from 'axios';

const API = axios.create({
  baseURL: '',
});

export const uploadDetectionAPI = {
  uploadImage: (formData) => API.post('/api/v1/upload/image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  uploadVideo: (formData) => API.post('/api/v1/upload/video', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  getStatus: (jobId) => API.get(`/api/v1/upload/status/${jobId}`),
  getHistory: () => API.get('/api/v1/upload/history'),
  getResult: (jobId) => API.get(`/api/v1/upload/result/${jobId}`),
  deleteHistory: (jobId) => API.delete(`/api/v1/upload/history/${jobId}`),
};

export default uploadDetectionAPI;
