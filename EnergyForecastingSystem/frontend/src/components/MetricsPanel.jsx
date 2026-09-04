import React from 'react';

const MetricsPanel = ({ modelName = 'XGBoost', mae = 13.95, rmse = 17.70, mape = 4.03, r2 = 0.9594 }) => {
  return (
    <div style={{
      display: 'flex',
      gap: '1.5rem',
      background: 'rgba(6, 182, 212, 0.05)',
      border: '1px solid rgba(6, 182, 212, 0.2)',
      borderRadius: '8px',
      padding: '0.8rem 1.25rem',
      fontSize: '0.85rem',
      alignItems: 'center',
      marginBottom: '1rem'
    }}>
      <div>Model: <strong style={{ color: '#fff' }}>{modelName}</strong></div>
      <div>MAE: <strong style={{ color: '#06b6d4' }}>{mae} MU</strong></div>
      <div>RMSE: <strong style={{ color: '#6366f1' }}>{rmse} MU</strong></div>
      <div>MAPE: <strong style={{ color: '#10b981' }}>{mape}%</strong></div>
      <div>R² Score: <strong style={{ color: '#f59e0b' }}>{r2}</strong></div>
    </div>
  );
};

export default MetricsPanel;
