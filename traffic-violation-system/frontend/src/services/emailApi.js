import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const emailAPI = {
  getStatus: () => API.get('/api/v1/email/status'),
  getLogs: () => API.get('/api/v1/email/logs'),
  getSettings: () => API.get('/api/v1/email/settings'),
  updateSettings: (settings) => API.put('/api/v1/email/settings', settings),
  sendTestEmail: (recipient_email) => API.post('/api/v1/email/send-test', { recipient_email }),
  sendViolation: (violationId) => API.post(`/api/v1/email/send-violation/${violationId}`),
};
