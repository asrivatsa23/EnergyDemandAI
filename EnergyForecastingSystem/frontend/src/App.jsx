import { useEffect, useState } from "react";
import "./App.css";

import Header from "./components/Header";
import ModelSelector from "./components/ModelSelector";
import CsvUploader from "./components/CsvUploader";
import MetricsPanel from "./components/MetricsPanel";
import ForecastChart from "./components/ForecastChart";
import ShapExplanation from "./components/ShapExplanation";
import { fetchModels, fetchMetrics, uploadCsvForPrediction } from "./api";

export default function App() {
  const [models, setModels] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchModels()
      .then((data) => {
        setModels(data.models);
        setSelectedModelId(data.default);
      })
      .catch(() => setError("Could not reach the backend API."));
  }, []);

  useEffect(() => {
    if (!selectedModelId) return;
    fetchMetrics(selectedModelId)
      .then(setMetrics)
      .catch(() => setError("Could not reach the backend API."));
    // Switching models invalidates the previous result/explanation.
    setResult(null);
  }, [selectedModelId]);

  const handleUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await uploadCsvForPrediction(file, selectedModelId);

      if (!data.success) {
        setError(data.error || "The prediction failed.");
        return;
      }

      setResult(data);
      setMetrics({
        model_name: data.model_name,
        mae: data.mae,
        r2: data.r2,
      });
    } catch (err) {
      const backendMessage = err?.response?.data?.error;
      setError(backendMessage || "Could not reach the backend API.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <Header />

      <main className="dashboard-grid">
        <section className="left-column">
          <ModelSelector
            models={models}
            selectedId={selectedModelId}
            onSelect={setSelectedModelId}
            disabled={isLoading}
          />
          <CsvUploader onUpload={handleUpload} isLoading={isLoading} />
          <MetricsPanel
            metrics={metrics}
            prediction={result ? result.prediction : null}
          />
          {error && <div className="error-banner">{error}</div>}
        </section>

        <section className="right-column">
          {result ? (
            <>
              <ForecastChart
                inputValues={result.input_values}
                timestamps={result.timestamps}
                prediction={result.prediction}
              />
              <ShapExplanation shap={result.shap} prediction={result.prediction} />
            </>
          ) : (
            <div className="card empty-state">
              <p>
                Upload a CSV with at least 24 hourly <code>AEP_MW</code>{" "}
                readings to see the forecast and its SHAP explanation here.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
