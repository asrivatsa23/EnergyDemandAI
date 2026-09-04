import React from 'react';
import { Cpu } from 'lucide-react';

const ModelSelector = ({ models = [], selectedModel, onSelectModel }) => {
  return (
    <div className="control-group">
      <label className="control-label">
        <Cpu size={15} className="text-cyan-400" />
        Forecasting Model:
      </label>
      <select
        className="select-control"
        value={selectedModel}
        onChange={(e) => onSelectModel(e.target.value)}
      >
        {models.map((m) => (
          <option key={m.id} value={m.id}>
            {m.name} {m.r2 ? `(R²: ${m.r2})` : ''}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ModelSelector;
