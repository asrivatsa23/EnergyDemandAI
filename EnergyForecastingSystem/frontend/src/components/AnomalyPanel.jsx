import React from 'react';
import { AlertTriangle, ShieldCheck } from 'lucide-react';

const AnomalyPanel = ({ anomalies = {} }) => {
  const { total_anomalies = 0, anomaly_rate_percent = 0, anomalies: list = [] } = anomalies;

  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <AlertTriangle className="text-amber-400" size={18} />
          Demand Anomaly Detection (Isolation Forest & Z-Score)
        </h3>
        <span style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
          Detected: <strong style={{ color: '#f59e0b' }}>{total_anomalies} anomalies</strong> ({anomaly_rate_percent}%)
        </span>
      </div>

      {list.length === 0 ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', padding: '1.5rem 0' }}>
          <ShieldCheck size={20} />
          <span>No statistical demand anomalies detected in historical window. Grid stability nominal.</span>
        </div>
      ) : (
        <div className="data-table-container">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Observed Demand</th>
                <th>Z-Score</th>
                <th>Anomaly Type</th>
                <th>Severity</th>
              </tr>
            </thead>
            <tbody>
              {list.slice(0, 8).map((a, i) => (
                <tr key={i}>
                  <td>{a.timestamp}</td>
                  <td style={{ fontWeight: '700' }}>{a.demand} MU</td>
                  <td style={{ color: a.z_score > 0 ? '#f59e0b' : '#06b6d4' }}>{a.z_score}</td>
                  <td>{a.type}</td>
                  <td>
                    <span style={{
                      padding: '0.2rem 0.5rem',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: '700',
                      background: a.severity === 'High' ? 'rgba(244, 63, 94, 0.15)' : 'rgba(245, 158, 11, 0.15)',
                      color: a.severity === 'High' ? '#f43f5e' : '#f59e0b'
                    }}>
                      {a.severity}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default AnomalyPanel;
