import axios from 'axios';

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
});

export const scanCode = (code) => API.post('/scan/', { code });
export const checkHealth = () => API.get('/scan/health/');

export default API;
