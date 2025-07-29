import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const analyzeText = async (text) => {
  const formData = new FormData();
  formData.append('text', text);
  const response = await axios.post(`${API_BASE}/analyze`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const analyzeCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await axios.post(`${API_BASE}/analyze_csv`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
}; 