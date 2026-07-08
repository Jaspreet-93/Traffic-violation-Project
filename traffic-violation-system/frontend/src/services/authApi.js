import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authAPI = {
  register: (payload) => API.post('/api/v1/auth/register', payload),
  login: (payload) => API.post('/api/v1/auth/login', payload),
  updateProfile: (userId, payload) => API.put(`/api/v1/auth/profile/${userId}`, payload),
  changePassword: (userId, payload) => API.put(`/api/v1/auth/change-password/${userId}`, payload),
  forgotPassword: (payload) => API.post('/api/v1/auth/forgot-password', payload),
};

export default authAPI;
