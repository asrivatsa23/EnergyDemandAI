import React from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import { Sun } from 'lucide-react';

const WeatherChart = ({ history = [] }) => {
  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <Sun size={18} className="text-amber-400" />
          Weather vs Demand Correlations
        </h3>
      </div>
      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <LineChart data={history.slice(-72)} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.06)" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" tickFormatter={(s) => s ? s.split(' ')[1] || s : ''} />
            <YAxis yAxisId="left" stroke="#06b6d4" unit=" MU" />
            <YAxis yAxisId="right" orientation="right" stroke="#f59e0b" unit="°C" />
            <Tooltip contentStyle={{ backgroundColor: '#0e1626', borderColor: 'rgba(6, 182, 212, 0.3)', borderRadius: '8px', color: '#fff' }} />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="demand" name="Demand (MU)" stroke="#06b6d4" strokeWidth={2} dot={false} />
            <Line yAxisId="right" type="monotone" dataKey="temperature" name="Temperature (°C)" stroke="#f59e0b" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default WeatherChart;
