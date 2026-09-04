import React from 'react';
import { Cpu, ArrowUpRight, ArrowDownRight, Info } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts';

const ShapExplanation = ({ explanation = {} }) => {
  const { base_value, features = [], summary } = explanation;

  const topFeatures = features.slice(0, 10);

  return (
    <div className="chart-card">
      <div className="card-header">
        <h3 className="card-title">
          <Cpu className="text-cyan-400" size={18} />
          Explainable AI (SHAP & LIME Feature Attribution)
        </h3>
        {base_value && (
          <span style={{ fontSize: '0.85rem', color: '#9ca3af' }}>
            Base Demand Value: <strong style={{ color: '#fff' }}>{base_value} MU</strong>
          </span>
        )}
      </div>

      {summary && (
        <div style={{
          background: 'rgba(6, 182, 212, 0.08)',
          borderLeft: '4px solid #06b6d4',
          padding: '0.9rem 1.2rem',
          borderRadius: '0 8px 8px 0',
          marginBottom: '1.5rem',
          fontSize: '0.9rem',
          color: '#e5e7eb',
          display: 'flex',
          gap: '0.75rem',
          alignItems: 'center'
        }}>
          <Info size={20} className="text-cyan-400" style={{ flexShrink: 0 }} />
          <span>{summary}</span>
        </div>
      )}

      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <BarChart data={topFeatures} layout="vertical" margin={{ top: 10, right: 30, left: 100, bottom: 10 }}>
            <XAxis type="number" stroke="#9ca3af" />
            <YAxis dataKey="feature" type="category" stroke="#9ca3af" style={{ fontSize: '0.8rem' }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#0e1626', borderColor: 'rgba(6, 182, 212, 0.3)', borderRadius: '8px', color: '#fff' }}
              formatter={(val, name, props) => [`${val} (${props.payload.direction})`, 'Contribution']}
            />
            <Bar dataKey="contribution">
              {topFeatures.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.direction === 'positive' ? '#10b981' : '#f43f5e'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="data-table-container" style={{ marginTop: '1.5rem' }}>
        <table className="custom-table">
          <thead>
            <tr>
              <th>Feature Name</th>
              <th>Current Value</th>
              <th>SHAP Contribution</th>
              <th>Impact Direction</th>
            </tr>
          </thead>
          <tbody>
            {topFeatures.map((f, i) => (
              <tr key={i}>
                <td style={{ fontWeight: '600' }}>{f.feature}</td>
                <td>{f.value}</td>
                <td style={{ fontWeight: '700', color: f.direction === 'positive' ? '#10b981' : '#f43f5e' }}>
                  {f.contribution > 0 ? `+${f.contribution}` : f.contribution} MU
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: f.direction === 'positive' ? '#10b981' : '#f43f5e' }}>
                    {f.direction === 'positive' ? <ArrowUpRight size={16} /> : <ArrowDownRight size={16} />}
                    <span style={{ textTransform: 'capitalize', fontSize: '0.85rem' }}>{f.direction} Impact</span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ShapExplanation;
