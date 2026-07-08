import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const officerEmailAPI = {
  getEmails: () => API.get('/api/v1/officer-emails'),
  addEmail: (payload) => API.post('/api/v1/officer-emails', payload),
  updateEmail: (id, payload) => API.put(`/api/v1/officer-emails/${id}`, payload),
  deleteEmail: (id) => API.delete(`/api/v1/officer-emails/${id}`),
  updateStatus: (id, active) => API.put(`/api/v1/officer-emails/${id}/status`, { active }),
  setPrimary: (id) => API.put(`/api/v1/officer-emails/${id}/primary`),
};

export default officerEmailAPI;
