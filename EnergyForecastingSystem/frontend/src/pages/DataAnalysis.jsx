import React from 'react';
import WeatherChart from '../components/WeatherChart';
import RenewableChart from '../components/RenewableChart';
import AnomalyPanel from '../components/AnomalyPanel';

const DataAnalysis = ({ historyData, anomalyData }) => {
  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Exploratory Data & Grid Feature Analysis</h1>
          <p className="page-subtitle">
            Historical demand trends, weather correlation, renewable generation mix, and holiday/seasonal patterns
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '1.5rem' }}>
        <WeatherChart history={historyData} />
        <RenewableChart history={historyData} />
      </div>

      <AnomalyPanel anomalies={anomalyData} />
    </div>
  );
};

export default DataAnalysis;
