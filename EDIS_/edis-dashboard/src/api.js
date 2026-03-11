import axios from "axios";

export const analyzeEcosystem = (lat, lon) =>
  axios.post("http://localhost:8000/analyze/ecosystem", {
    latitude: lat,
    longitude: lon,
  });

export const downloadReport = () =>
  window.open("http://localhost:8000/download/report");
