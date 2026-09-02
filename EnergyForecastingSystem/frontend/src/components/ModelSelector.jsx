export default function ModelSelector({ models, selectedId, onSelect, disabled }) {
  if (!models || models.length === 0) return null;

  return (
    <div className="card model-selector">
      <h2>Model</h2>
      <p className="muted">Choose which trained model runs the forecast.</p>

      <div className="model-options">
        {models.map((m) => (
          <label
            key={m.id}
            className={`model-option ${selectedId === m.id ? "selected" : ""}`}
          >
            <input
              type="radio"
              name="model"
              value={m.id}
              checked={selectedId === m.id}
              disabled={disabled}
              onChange={() => onSelect(m.id)}
            />
            <div className="model-option-body">
              <div className="model-option-title">
                <span>{m.name}</span>
                <span className="model-option-r2">R² {m.r2}</span>
              </div>
              <p className="model-option-desc">{m.description}</p>
              {m.requires_datetime && (
                <span className="model-badge">Needs Datetime column</span>
              )}
            </div>
          </label>
        ))}
      </div>
    </div>
  );
}
