import React from 'react';
import { Award } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

const ModelComparison = ({ comparison = [] }) => {
  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <Award className="text-indigo-400" size={18} />
          Model Evaluation Benchmark (MAE, RMSE, MAPE & R²)
        </h3>
      </div>

      <div style={{ width: '100%', height: 320, marginBottom: '2rem' }}>
        <ResponsiveContainer>
          <BarChart data={comparison} margin={{ top: 10, right: 30, left: 10, bottom: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.06)" />
            <XAxis dataKey="Model" stroke="#9ca3af" style={{ fontSize: '0.8rem' }} />
            <YAxis stroke="#9ca3af" />
            <Tooltip contentStyle={{ backgroundColor: '#0e1626', borderColor: 'rgba(6, 182, 212, 0.3)', borderRadius: '8px', color: '#fff' }} />
            <Legend />
            <Bar dataKey="MAE" name="Mean Absolute Error (Lower is better)" fill="#06b6d4" radius={[4, 4, 0, 0]} />
            <Bar dataKey="RMSE" name="Root Mean Squared Error" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="data-table-container">
        <table className="custom-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>MAE (MU)</th>
              <th>RMSE (MU)</th>
              <th>MAPE (%)</th>
              <th>R² Score</th>
              <th>Train Time (s)</th>
              <th>Predict Time (s)</th>
            </tr>
          </thead>
          <tbody>
            {comparison.map((m, i) => (
              <tr key={i}>
                <td style={{ fontWeight: '700' }}>{m.Model}</td>
                <td>{m.MAE}</td>
                <td>{m.RMSE}</td>
                <td>{m["MAPE (%)"]}%</td>
                <td style={{ fontWeight: '700', color: m.R2 > 0.9 ? '#10b981' : (m.R2 > 0.7 ? '#06b6d4' : '#f43f5e') }}>
                  {m.R2}
                </td>
                <td>{m["Training Time (s)"]}s</td>
                <td>{m["Prediction Time (s)"]}s</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelComparison;
