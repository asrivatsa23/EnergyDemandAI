import React from 'react';
import { Clock } from 'lucide-react';

const ForecastHorizon = ({ horizon, onSelectHorizon }) => {
  const options = [
    { value: 1, label: '1 Hour' },
    { value: 6, label: '6 Hours' },
    { value: 24, label: '24 Hours (Next Day)' },
    { value: 168, label: '7 Days (Weekly)' },
  ];

  return (
    <div className="control-group">
      <label className="control-label">
        <Clock size={15} className="text-cyan-400" />
        Forecast Horizon:
      </label>
      <select
        className="select-control"
        value={horizon}
        onChange={(e) => onSelectHorizon(Number(e.target.value))}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ForecastHorizon;
