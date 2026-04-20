import axios from "axios";

// Use your deployed backend URL instead of localhost
const BASE_URL = "https://edis-backend.azurewebsites.net";

export const analyzeEcosystem = (lat, lon) =>
  axios.post(`${BASE_URL}/analyze/ecosystem`, {
    latitude: lat,
    longitude: lon,
  });

export const downloadReport = () =>
  window.open(`${BASE_URL}/download/report`);
