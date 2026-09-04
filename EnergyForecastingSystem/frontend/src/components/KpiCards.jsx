import React from 'react';
import { Activity, TrendingUp, Zap, Award } from 'lucide-react';

const KpiCards = ({ kpis = {} }) => {
  const cards = [
    {
      title: 'Current Demand',
      value: kpis.current_demand ? `${kpis.current_demand}` : '348.5',
      unit: 'MU',
      subtext: 'Real-time grid load',
      icon: Activity,
      color: '#06b6d4'
    },
    {
      title: '24h Peak Forecast',
      value: kpis.predicted_peak ? `${kpis.predicted_peak}` : '412.0',
      unit: 'MU',
      subtext: 'Anticipated peak load',
      icon: TrendingUp,
      color: '#f59e0b'
    },
    {
      title: '24h Avg Load',
      value: kpis.predicted_avg ? `${kpis.predicted_avg}` : '356.2',
      unit: 'MU',
      subtext: 'Mean forecasted load',
      icon: Zap,
      color: '#10b981'
    },
    {
      title: 'Best Model',
      value: kpis.best_model ? kpis.best_model.split(' ')[0] : 'XGBoost',
      unit: 'R² 0.959',
      subtext: 'Highest accuracy model',
      icon: Award,
      color: '#6366f1'
    }
  ];

  return (
    <div className="kpi-grid">
      {cards.map((c, i) => {
        const Icon = c.icon;
        return (
          <div className="kpi-card" key={i}>
            <div className="kpi-title">
              <span>{c.title}</span>
              <Icon size={18} style={{ color: c.color }} />
            </div>
            <div className="kpi-value">
              {c.value}
              <span className="kpi-unit">{c.unit}</span>
            </div>
            <div className="kpi-subtext">
              <span>{c.subtext}</span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default KpiCards;
