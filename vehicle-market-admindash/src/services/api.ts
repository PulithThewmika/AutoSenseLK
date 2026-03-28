import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Analytics API
export const getMarketSummary = async () => {
  const { data } = await api.get('/analytics/summary');
  return data;
};

export const getBrandAnalytics = async () => {
  const { data } = await api.get('/analytics/daily/brands');
  return data;
};

export const getDailyHistory = async () => {
  const { data } = await api.get('/analytics/daily/history', { params: { days: 30 } });
  return data;
};

// Scraper API
export const getScrapeStatus = async () => {
  const { data } = await api.get('/scrape/status');
  return data;
};

// System API (using basic health endpoint)
export const getHealth = async () => {
  const { data } = await axios.get('http://localhost:8000/health');
  return data;
};

export default api;
