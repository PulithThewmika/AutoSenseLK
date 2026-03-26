import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL + '/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
});

export const getMakes = () => api.get('/makes/').then(res => res.data);
export const getModels = (make: string) => api.get(`/makes/${make}/models`).then(res => res.data);
export const getSummary = () => api.get('/analytics/summary').then(res => res.data);
export const getTrends = (make?: string, model?: string, months: number = 12) => {
  let url = `/analytics/trends?months=${months}`;
  if (make) url += `&make=${encodeURIComponent(make)}`;
  if (model) url += `&model=${encodeURIComponent(model)}`;
  return api.get(url).then(res => res.data);
};
export const getListings = (page: number = 1, size: number = 20) =>
  api.get(`/listings/?page=${page}&size=${size}`).then(res => res.data);
export const getAvgPrice = (make: string, model: string) =>
  api.get(`/analytics/avg-price?make=${encodeURIComponent(make)}&model=${encodeURIComponent(model)}`).then(res => res.data);
export const getDepreciation = (make?: string, model?: string) => {
  let url = '/analytics/depreciation';
  if (make) url += `?make=${encodeURIComponent(make)}`;
  if (model) url += `${make ? '&' : '?'}model=${encodeURIComponent(model)}`;
  return api.get(url).then(res => res.data);
};
export const getMileage = (make?: string, model?: string) => {
  let url = '/analytics/mileage';
  if (make) url += `?make=${encodeURIComponent(make)}`;
  if (model) url += `${make ? '&' : '?'}model=${encodeURIComponent(model)}`;
  return api.get(url).then(res => res.data);
};
export const getDailyBrands = () => api.get('/analytics/daily/brands').then(res => res.data);
export const getDailyHistory = (scope: string = 'market', brand?: string, days: number = 30) => {
  let url = `/analytics/daily/history?scope=${scope}&days=${days}`;
  if (brand) url += `&brand=${encodeURIComponent(brand)}`;
  return api.get(url).then(res => res.data);
};
