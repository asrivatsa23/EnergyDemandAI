import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Forecast from './pages/Forecast';
import ModelComparison from './pages/ModelComparison';
import Explainability from './pages/Explainability';
import DataAnalysis from './pages/DataAnalysis';
import LoadingState from './components/LoadingState';
import ErrorState from './components/ErrorState';

import {
  fetchHealth,
  fetchModels,
  fetchStates,
  fetchForecast,
  fetchHistory,
  fetchModelComparison,
  fetchExplanation,
  fetchAnomalies
} from './api';

import './App.css';

function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [isOnline, setIsOnline] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Selections
  const [states, setStates] = useState(['Maharashtra', 'Gujarat', 'Tamil Nadu', 'Karnataka', 'Delhi', 'Uttar Pradesh']);
  const [selectedState, setSelectedState] = useState('Maharashtra');

  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('xgboost');
  const [horizon, setHorizon] = useState(24);

  // Data states
  const [forecastData, setForecastData] = useState([]);
  const [kpis, setKpis] = useState({});
  const [historyData, setHistoryData] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  const [explanationData, setExplanationData] = useState({});
  const [anomalyData, setAnomalyData] = useState({});

  const loadInitialData = async () => {
    setLoading(true);
    setError(null);
    try {
      // 1. Health check
      const healthRes = await fetchHealth();
      setIsOnline(healthRes.status === 'online');

      // 2. States & Models
      const statesRes = await fetchStates();
      if (statesRes.states) setStates(statesRes.states);

      const modelsRes = await fetchModels();
      if (modelsRes.models) setModels(modelsRes.models);

      // 3. Forecast
      const fcRes = await fetchForecast(selectedModel, horizon, selectedState);
      if (fcRes.forecast) setForecastData(fcRes.forecast);
      if (fcRes.kpis) setKpis(fcRes.kpis);

      // 4. History
      const histRes = await fetchHistory(selectedState, 168);
      if (histRes.history) setHistoryData(histRes.history);

      // 5. Model Comparison
      const compRes = await fetchModelComparison();
      if (compRes.comparison) setComparisonData(compRes.comparison);

      // 6. Explainability
      const expRes = await fetchExplanation(selectedModel);
      if (expRes.explanation) setExplanationData(expRes.explanation);

      // 7. Anomalies
      const anomRes = await fetchAnomalies();
      if (anomRes.data) setAnomalyData(anomRes.data);

    } catch (err) {
      console.error("Error loading application data:", err);
      setError("Unable to connect to EnergyDemandAI backend REST server at http://localhost:5000.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // Update forecast & explanation when model/horizon/state changes
  useEffect(() => {
    if (!isOnline) return;

    const updateForecast = async () => {
      try {
        const fcRes = await fetchForecast(selectedModel, horizon, selectedState);
        if (fcRes.forecast) setForecastData(fcRes.forecast);
        if (fcRes.kpis) setKpis(fcRes.kpis);

        const expRes = await fetchExplanation(selectedModel);
        if (expRes.explanation) setExplanationData(expRes.explanation);
      } catch (err) {
        console.error("Error updating forecast:", err);
      }
    };

    updateForecast();
  }, [selectedModel, horizon, selectedState, isOnline]);

  return (
    <div className="app-container">
      <Header activePage={activePage} setActivePage={setActivePage} isOnline={isOnline} />

      <main className="page-content">
        {loading ? (
          <LoadingState message="Initializing EnergyDemandAI Grid Intelligence Engine..." />
        ) : error ? (
          <ErrorState message={error} onRetry={loadInitialData} />
        ) : (
          <>
            {activePage === 'dashboard' && (
              <Dashboard
                states={states}
                selectedState={selectedState}
                onSelectState={setSelectedState}
                models={models}
                selectedModel={selectedModel}
                onSelectModel={setSelectedModel}
                forecastData={forecastData}
                kpis={kpis}
                historyData={historyData}
                anomalyData={anomalyData}
              />
            )}

            {activePage === 'forecast' && (
              <Forecast
                states={states}
                selectedState={selectedState}
                onSelectState={setSelectedState}
                horizon={horizon}
                onSelectHorizon={setHorizon}
                models={models}
                selectedModel={selectedModel}
                onSelectModel={setSelectedModel}
                forecastData={forecastData}
              />
            )}

            {activePage === 'comparison' && (
              <ModelComparison comparisonData={comparisonData} />
            )}

            {activePage === 'explainability' && (
              <Explainability
                models={models}
                selectedModel={selectedModel}
                onSelectModel={setSelectedModel}
                explanationData={explanationData}
              />
            )}

            {activePage === 'analysis' && (
              <DataAnalysis historyData={historyData} anomalyData={anomalyData} />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
