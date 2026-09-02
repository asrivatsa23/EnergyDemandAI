export default function MetricsPanel({ metrics, prediction }) {
  return (
    <div className="card metrics-panel">
      <div className="metric">
        <span className="metric-label">Model</span>
        <span className="metric-value">{metrics?.model_name ?? "—"}</span>
      </div>
      <div className="metric">
        <span className="metric-label">MAE</span>
        <span className="metric-value">{metrics?.mae ?? "—"}</span>
      </div>
      <div className="metric">
        <span className="metric-label">R²</span>
        <span className="metric-value">{metrics?.r2 ?? "—"}</span>
      </div>
      <div className="metric highlight">
        <span className="metric-label">Next-hour forecast</span>
        <span className="metric-value">
          {prediction !== null ? `${prediction.toLocaleString()} MW` : "—"}
        </span>
      </div>
    </div>
  );
}
