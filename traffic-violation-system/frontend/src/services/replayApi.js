import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const replayAPI = {
  listReplays: () => API.get('/api/v1/replay/list'),
  getReplayDetails: (id) => API.get(`/api/v1/replay/${id}`),
  getTimeline: (id) => API.get(`/api/v1/replay/timeline/${id}`),
  getFrame: (id, num) => API.get(`/api/v1/replay/frame/${id}/${num}`),
};

export default replayAPI;
