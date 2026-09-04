import React from 'react';
import StateSelector from '../components/StateSelector';
import ModelSelector from '../components/ModelSelector';
import KpiCards from '../components/KpiCards';
import ForecastChart from '../components/ForecastChart';
import AnomalyPanel from '../components/AnomalyPanel';
import WeatherChart from '../components/WeatherChart';

const Dashboard = ({
  states,
  selectedState,
  onSelectState,
  models,
  selectedModel,
  onSelectModel,
  forecastData,
  kpis,
  historyData,
  anomalyData
}) => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Executive Demand Analytics Dashboard</h1>
          <p className="page-subtitle">
            Real-time Indian Electricity Demand Overview & 24-Hour Predictive Support
          </p>
        </div>
      </div>

      <div className="controls-bar">
        <StateSelector states={states} selectedState={selectedState} onSelectState={onSelectState} />
        <ModelSelector models={models} selectedModel={selectedModel} onSelectModel={onSelectModel} />
      </div>

      <KpiCards kpis={kpis} />

      <ForecastChart data={forecastData} title={`24-Hour Demand Forecast for ${selectedState}`} />

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))', gap: '1.5rem' }}>
        <WeatherChart history={historyData} />
        <AnomalyPanel anomalies={anomalyData} />
      </div>
    </div>
  );
};

export default Dashboard;
