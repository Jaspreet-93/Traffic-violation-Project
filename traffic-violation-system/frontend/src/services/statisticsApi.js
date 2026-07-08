import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const statisticsAPI = {
  getOverview: () => API.get('/api/v1/statistics'),
  getDaily: () => API.get('/api/v1/statistics/daily'),
  getWeekly: () => API.get('/api/v1/statistics/weekly'),
  getMonthly: () => API.get('/api/v1/statistics/monthly'),
  getPerformance: () => API.get('/api/v1/statistics/performance'),
};

export default statisticsAPI;
