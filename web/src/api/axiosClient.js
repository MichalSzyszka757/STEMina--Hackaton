// src/api/axiosClient.js
import axios from 'axios';

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api/v1", // Zmienna środowiskowa
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;