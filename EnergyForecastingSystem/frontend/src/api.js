/**
 * EnergyDemandAI - Centralized API Client
 * Handles all REST API communications between React frontend and Flask backend.
 */

import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchHealth = async () => {
  const res = await api.get('/health');
  return res.data;
};

export const fetchModels = async () => {
  const res = await api.get('/models');
  return res.data;
};

export const fetchStates = async () => {
  const res = await api.get('/states');
  return res.data;
};

export const fetchRegions = async () => {
  const res = await api.get('/regions');
  return res.data;
};

export const fetchHistory = async (state = 'Maharashtra', limit = 168) => {
  const res = await api.get(`/history?state=${encodeURIComponent(state)}&limit=${limit}`);
  return res.data;
};

export const fetchForecast = async (model = 'xgboost', horizon = 24, state = 'Maharashtra') => {
  const res = await api.get(`/forecast?model=${model}&horizon=${horizon}&state=${encodeURIComponent(state)}`);
  return res.data;
};

export const fetchModelComparison = async () => {
  const res = await api.get('/model-comparison');
  return res.data;
};

export const fetchExplanation = async (model = 'xgboost') => {
  const res = await api.get(`/explain?model=${model}`);
  return res.data;
};

export const fetchAnomalies = async () => {
  const res = await api.get('/anomalies');
  return res.data;
};

export const uploadAndPredict = async (file, model = 'xgboost') => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('model', model);

  const res = await api.post('/predict', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data;
};

export default api;
