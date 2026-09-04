import React, { useState } from 'react';
import StateSelector from '../components/StateSelector';
import ForecastHorizon from '../components/ForecastHorizon';
import ModelSelector from '../components/ModelSelector';
import ForecastChart from '../components/ForecastChart';
import ForecastTable from '../components/ForecastTable';
import CsvUploader from '../components/CsvUploader';
import MetricsPanel from '../components/MetricsPanel';

const Forecast = ({
  states,
  selectedState,
  onSelectState,
  horizon,
  onSelectHorizon,
  models,
  selectedModel,
  onSelectModel,
  forecastData,
  onUploadedPrediction
}) => {
  const [activeData, setActiveData] = useState(forecastData);
  const [customPrediction, setCustomPrediction] = useState(null);

  const displayData = customPrediction?.forecast || forecastData;
  const currentModelObj = models.find(m => m.id === selectedModel);

  const handleUploadComplete = (res) => {
    setCustomPrediction(res);
    if (onUploadedPrediction) onUploadedPrediction(res);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Electricity Demand Forecasting Engine</h1>
          <p className="page-subtitle">
            Multi-Horizon Time-Series Forecasting with Custom CSV Data Ingestion
          </p>
        </div>
      </div>

      <div className="controls-bar">
        <StateSelector states={states} selectedState={selectedState} onSelectState={onSelectState} />
        <ForecastHorizon horizon={horizon} onSelectHorizon={onSelectHorizon} />
        <ModelSelector models={models} selectedModel={selectedModel} onSelectModel={onSelectModel} />
      </div>

      {currentModelObj && (
        <MetricsPanel
          modelName={currentModelObj.name}
          mae={currentModelObj.mae}
          rmse={currentModelObj.rmse}
          mape={currentModelObj.mape}
          r2={currentModelObj.r2}
        />
      )}

      <ForecastChart
        data={displayData}
        title={`${horizon}-Hour Demand Forecast (${selectedState}) - Model: ${selectedModel.toUpperCase()}`}
      />

      <ForecastTable data={displayData} />

      <CsvUploader
        models={models}
        selectedModel={selectedModel}
        onPredictionComplete={handleUploadComplete}
      />
    </div>
  );
};

export default Forecast;
