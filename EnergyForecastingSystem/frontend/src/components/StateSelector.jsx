import React from 'react';
import { MapPin } from 'lucide-react';

const StateSelector = ({ states = [], selectedState, onSelectState }) => {
  return (
    <div className="control-group">
      <label className="control-label">
        <MapPin size={15} className="text-cyan-400" />
        State / Region:
      </label>
      <select
        className="select-control"
        value={selectedState}
        onChange={(e) => onSelectState(e.target.value)}
      >
        {states.map((st) => (
          <option key={st} value={st}>
            {st}
          </option>
        ))}
      </select>
    </div>
  );
};

export default StateSelector;
