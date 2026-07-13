import axios from 'axios';

const API = axios.create({
  baseURL: '',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const evidenceAPI = {
  getAll: (page = 1, limit = 20, config = {}) => API.get(`/api/v1/evidence`, { params: { page, limit }, ...config }),
  getById: (id) => API.get(`/api/v1/evidence/${id}`),
  getMetadata: (id) => API.get(`/api/v1/evidence/metadata/${id}`),
  getIntegrity: (id) => API.get(`/api/v1/evidence/integrity/${id}`),
  deleteEvidence: (id) => API.delete(`/api/v1/evidence/${id}`),
  getDownloadUrl: (id) => `/api/v1/evidence/download/${id}`,
  getPreviewUrl: (id) => `/api/v1/evidence/preview/${id}`,
  search: (params, config = {}) => API.get('/api/v1/evidence/search', { params, ...config }),
  getDownloadOriginalUrl: (id) => `/api/v1/evidence/download/original/${id}`,
  getDownloadAnnotatedUrl: (id) => `/api/v1/evidence/download/annotated/${id}`,
};

export default evidenceAPI;
