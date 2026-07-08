import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const settingsAPI = {
  getSettings: () => API.get('/api/v1/settings'),
  updateSettings: (data) => API.put('/api/v1/settings', data),
};

export default settingsAPI;
