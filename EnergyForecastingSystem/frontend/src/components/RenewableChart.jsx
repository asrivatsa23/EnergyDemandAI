import React from 'react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import { Wind } from 'lucide-react';

const RenewableChart = ({ history = [] }) => {
  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <Wind size={18} className="text-emerald-400" />
          Renewable Energy Generation Mix (Solar, Wind & Hydro)
        </h3>
      </div>
      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <AreaChart data={history.slice(-72)} margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.06)" />
            <XAxis dataKey="timestamp" stroke="#9ca3af" tickFormatter={(s) => s ? s.split(' ')[1] || s : ''} />
            <YAxis stroke="#9ca3af" unit=" MU" />
            <Tooltip contentStyle={{ backgroundColor: '#0e1626', borderColor: 'rgba(6, 182, 212, 0.3)', borderRadius: '8px', color: '#fff' }} />
            <Legend />
            <Area type="monotone" dataKey="solar" name="Solar Gen (MU)" stackId="1" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.6} />
            <Area type="monotone" dataKey="wind" name="Wind Gen (MU)" stackId="1" stroke="#10b981" fill="#10b981" fillOpacity={0.6} />
            <Area type="monotone" dataKey="hydro" name="Hydro Gen (MU)" stackId="1" stroke="#6366f1" fill="#6366f1" fillOpacity={0.6} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default RenewableChart;
