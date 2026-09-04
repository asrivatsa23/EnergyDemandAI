import React from 'react';
import { Download } from 'lucide-react';

const ForecastTable = ({ data = [] }) => {
  const downloadCSV = () => {
    if (!data || data.length === 0) return;
    const headers = ["Timestamp", "Hour", "Predicted Demand (MU)"];
    const rows = data.map(d => [d.timestamp, d.hour, d.predicted_demand]);
    const csvContent = [headers.join(","), ...rows.map(r => r.join(","))].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "energy_demand_forecast.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">Forecast Table View</h3>
        <button className="btn-primary" onClick={downloadCSV}>
          <Download size={15} />
          Download CSV
        </button>
      </div>

      <div className="data-table-container">
        <table className="custom-table">
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Hour</th>
              <th>Predicted Demand (MU)</th>
              <th>Load Category</th>
            </tr>
          </thead>
          <tbody>
            {data.slice(0, 24).map((row, idx) => {
              const category = row.predicted_demand > 380 ? 'Peak' : (row.predicted_demand < 330 ? 'Off-Peak' : 'Normal');
              const badgeStyle = category === 'Peak' ? { color: '#f59e0b', background: 'rgba(245, 158, 11, 0.1)' } :
                (category === 'Off-Peak' ? { color: '#06b6d4', background: 'rgba(6, 182, 212, 0.1)' } : { color: '#10b981', background: 'rgba(16, 185, 129, 0.1)' });

              return (
                <tr key={idx}>
                  <td>{row.timestamp}</td>
                  <td>{row.hour}:00</td>
                  <td style={{ fontWeight: '700' }}>{row.predicted_demand} MU</td>
                  <td>
                    <span style={{ ...badgeStyle, padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: '600' }}>
                      {category}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ForecastTable;
