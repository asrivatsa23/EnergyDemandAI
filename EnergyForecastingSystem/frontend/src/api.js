import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export async function fetchModels() {
  const { data } = await api.get("/models");
  return data;
}

export async function fetchMetrics(modelId) {
  const { data } = await api.get("/metrics", { params: { model: modelId } });
  return data;
}

export async function uploadCsvForPrediction(file, modelId) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("model", modelId);

  const { data } = await api.post("/predict", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return data;
}

export function downloadSampleCsvUrl() {
  return "/api/sample-csv";
}

export default api;
