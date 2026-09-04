import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';

const ForecastChart = ({ data = [], title = "24-Hour Ahead Electricity Demand Forecast" }) => {
  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
      </div>
      <div style={{ width: '100%', height: 380 }}>
        <ResponsiveContainer>
          <ComposedChart data={data} margin={{ top: 10, right: 30, left: 10, bottom: 20 }}>
            <defs>
              <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.06)" />
            <XAxis
              dataKey="timestamp"
              stroke="#9ca3af"
              tickFormatter={(str) => str ? str.split(' ')[1] || str : ''}
              style={{ fontSize: '0.8rem' }}
            />
            <YAxis
              stroke="#9ca3af"
              domain={['auto', 'auto']}
              unit=" MU"
              style={{ fontSize: '0.8rem' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0e1626',
                borderColor: 'rgba(6, 182, 212, 0.3)',
                borderRadius: '8px',
                color: '#fff'
              }}
            />
            <Legend wrapperStyle={{ paddingTop: '10px' }} />
            <Area
              type="monotone"
              dataKey="predicted_demand"
              name="Predicted Demand (MU)"
              stroke="#06b6d4"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#colorForecast)"
            />
            {data[0]?.actual_demand !== undefined && (
              <Line
                type="monotone"
                dataKey="actual_demand"
                name="Actual Demand (MU)"
                stroke="#10b981"
                strokeWidth={2}
                dot={false}
              />
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ForecastChart;
